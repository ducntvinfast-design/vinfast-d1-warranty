"""
SnapVF - Phần mềm chụp màn hình cho laptop (Windows ưu tiên, chạy được trên macOS/Linux).

Tính năng:
  * Chụp vùng chọn / toàn màn hình / cửa sổ đang mở / lặp lại vùng trước / hẹn giờ
  * Phím tắt toàn cục (tùy chỉnh được) + biểu tượng ở khay hệ thống
  * Tự lưu file theo thư mục ngày, tự copy vào clipboard (dán thẳng vào Zalo, Word, Excel...)
  * Trình chỉnh sửa: bút vẽ, mũi tên, khung, elip, tô sáng, chữ, làm mờ thông tin, đánh số, cắt ảnh
  * Cài đặt lưu tại %APPDATA%\\SnapVF\\config.json, có tùy chọn khởi động cùng Windows
"""
import ctypes
import datetime as dt
import io
import json
import math
import os
import queue
import subprocess
import sys
import tempfile
from pathlib import Path

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk

import mss
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pynput import keyboard

try:
    import pystray
except Exception:  # khay hệ thống là tùy chọn
    pystray = None

IS_WIN = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"

if IS_WIN:
    import ctypes.wintypes
    # Bật DPI-aware để tọa độ chuột khớp đúng pixel thật trên màn hình 125%/150%
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

APP_NAME = "SnapVF"
CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home() / ".config")) / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "save_dir": str(Path.home() / "Pictures" / "SnapVF"),
    "subfolder_by_date": True,           # Lưu vào thư mục con theo tháng: 2026-10/
    "filename_prefix": "Anh",            # Tên file: Anh_2026-10-13_09-30-15.png
    "format": "png",                     # png | jpg
    "jpg_quality": 90,
    "auto_save": True,
    "copy_to_clipboard": True,
    "open_editor": True,                 # Mở trình chỉnh sửa sau khi chụp
    "delay_seconds": 3,                  # Dùng cho chế độ "hẹn giờ"
    "autostart": False,
    "hotkeys": {
        "region": "<ctrl>+<shift>+a",
        "full": "<ctrl>+<shift>+f",
        "window": "<ctrl>+<shift>+w",
        "last": "<ctrl>+<shift>+r",
        "delay": "<ctrl>+<shift>+d",
    },
}

ACTION_LABELS = {
    "region": "Chụp vùng chọn",
    "full": "Chụp toàn màn hình",
    "window": "Chụp cửa sổ đang mở",
    "last": "Chụp lại vùng trước",
    "delay": "Chụp vùng sau X giây",
}


# ----------------------------------------------------------------- cấu hình
def load_config():
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            user = json.load(f)
        hotkeys = {**cfg["hotkeys"], **user.get("hotkeys", {})}
        cfg.update(user)
        cfg["hotkeys"] = hotkeys
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Không đọc được config:", e)
    return cfg


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def pretty_hotkey(combo):
    return "+".join(p.strip("<>").capitalize() for p in combo.split("+")) if combo else "—"


# ----------------------------------------------------------------- chụp / lưu / copy
def grab(region=None):
    """Chụp màn hình. region=None -> toàn bộ các màn hình. Trả về (ảnh, vùng)."""
    with mss.mss() as sct:
        mon = region or sct.monitors[0]
        shot = sct.grab(mon)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        return img, dict(mon)


def foreground_window_rect():
    if not IS_WIN:
        return None
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None
    rect = ctypes.wintypes.RECT()
    # DWMWA_EXTENDED_FRAME_BOUNDS = 9 -> khung thật, không gồm bóng đổ
    if ctypes.windll.dwmapi.DwmGetWindowAttribute(
            hwnd, 9, ctypes.byref(rect), ctypes.sizeof(rect)) != 0:
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top
    if w <= 0 or h <= 0:
        return None
    return {"left": rect.left, "top": rect.top, "width": w, "height": h}


def build_save_path(cfg):
    folder = Path(os.path.expandvars(os.path.expanduser(cfg["save_dir"])))
    if cfg.get("subfolder_by_date"):
        folder = folder / dt.datetime.now().strftime("%Y-%m")
    folder.mkdir(parents=True, exist_ok=True)
    prefix = cfg.get("filename_prefix", "").strip()
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = f"{prefix}_{stamp}" if prefix else stamp
    ext = "jpg" if cfg.get("format") == "jpg" else "png"
    path, i = folder / f"{base}.{ext}", 1
    while path.exists():
        path, i = folder / f"{base}_{i}.{ext}", i + 1
    return path


def write_image(img, path, cfg):
    path = Path(path)
    if path.suffix.lower() in (".jpg", ".jpeg"):
        img.convert("RGB").save(path, "JPEG", quality=int(cfg.get("jpg_quality", 90)))
    else:
        img.save(path, "PNG")
    return path


def copy_image(img):
    try:
        if IS_WIN:
            import win32clipboard
            buf = io.BytesIO()
            img.convert("RGB").save(buf, "BMP")
            data = buf.getvalue()[14:]  # bỏ header file BMP -> CF_DIB
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            finally:
                win32clipboard.CloseClipboard()
        elif IS_MAC:
            tmp = Path(tempfile.gettempdir()) / "snapvf_clip.png"
            img.save(tmp)
            subprocess.run(["osascript", "-e",
                            f'set the clipboard to (read (POSIX file "{tmp}") as «class PNGf»)'],
                           check=True)
        else:
            buf = io.BytesIO()
            img.save(buf, "PNG")
            subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-i"],
                           input=buf.getvalue(), check=True)
        return True
    except Exception as e:
        print("Copy clipboard lỗi:", e)
        return False


def open_path(path):
    path = str(path)
    if IS_WIN:
        os.startfile(path)
    elif IS_MAC:
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def set_autostart(enable):
    if not IS_WIN:
        return
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    try:
        if enable:
            if getattr(sys, "frozen", False):
                cmd = f'"{sys.executable}" --tray'
            else:
                pyw = Path(sys.executable).with_name("pythonw.exe")
                cmd = f'"{pyw}" "{Path(__file__).resolve()}" --tray'
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
    finally:
        winreg.CloseKey(key)


def load_font(size):
    for name in ("segoeui.ttf", "arial.ttf", "Arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def make_tray_icon():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((4, 14, 60, 54), 10, fill=(20, 110, 230))
    d.rectangle((22, 8, 42, 16), fill=(20, 110, 230))
    d.ellipse((20, 20, 44, 44), fill="white")
    d.ellipse((26, 26, 38, 38), fill=(20, 110, 230))
    return img


# ----------------------------------------------------------------- chọn vùng
class RegionSelector(tk.Toplevel):
    def __init__(self, app, img, mon, on_done):
        super().__init__(app.root)
        self.img, self.mon, self.on_done = img, mon, on_done
        self.start = None
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry(f"{mon['width']}x{mon['height']}+{mon['left']}+{mon['top']}")

        dim = Image.blend(img, Image.new("RGB", img.size, (0, 0, 0)), 0.45)
        self.bg = ImageTk.PhotoImage(dim)
        self.c = tk.Canvas(self, width=mon["width"], height=mon["height"],
                           highlightthickness=0, cursor="crosshair")
        self.c.pack(fill="both", expand=True)
        self.c.create_image(0, 0, anchor="nw", image=self.bg)
        self.crop_item = self.rect_item = self.size_item = None
        self.tk_crop = None

        # Gợi ý hiển thị ở góc trên màn hình chính (màn hình chính luôn bắt đầu tại 0,0)
        self.c.create_text(
            30 - mon["left"], 30 - mon["top"], anchor="nw",
            text="Kéo chuột để chọn vùng  •  Click đúp = toàn màn hình  •  Esc / chuột phải = hủy",
            fill="white", font=("Segoe UI", 13, "bold"), tags="hint")

        self.c.bind("<ButtonPress-1>", self._press)
        self.c.bind("<B1-Motion>", self._drag)
        self.c.bind("<ButtonRelease-1>", self._release)
        self.c.bind("<Double-Button-1>", lambda e: self._finish(self.img, None))
        self.c.bind("<Button-3>", lambda e: self._finish(None, None))
        self.bind("<Escape>", lambda e: self._finish(None, None))
        self.after(50, self._grab_focus)

    def _grab_focus(self):
        self.lift()
        self.focus_force()
        try:
            self.grab_set()
        except tk.TclError:
            pass

    def _box(self, e):
        x0, y0 = self.start
        x1 = min(max(e.x, 0), self.img.width)
        y1 = min(max(e.y, 0), self.img.height)
        return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)

    def _press(self, e):
        self.start = (e.x, e.y)
        self.c.delete("hint")

    def _drag(self, e):
        if not self.start:
            return
        x0, y0, x1, y1 = self._box(e)
        if x1 - x0 < 1 or y1 - y0 < 1:
            return
        self.tk_crop = ImageTk.PhotoImage(self.img.crop((x0, y0, x1, y1)))
        if self.crop_item is None:
            self.crop_item = self.c.create_image(x0, y0, anchor="nw", image=self.tk_crop)
            self.rect_item = self.c.create_rectangle(x0, y0, x1, y1, outline="#1e90ff", width=2)
            self.size_item = self.c.create_text(x0, y0 - 6, anchor="sw", fill="white",
                                                font=("Segoe UI", 11, "bold"))
        self.c.itemconfig(self.crop_item, image=self.tk_crop)
        self.c.coords(self.crop_item, x0, y0)
        self.c.coords(self.rect_item, x0, y0, x1, y1)
        self.c.coords(self.size_item, x0, max(y0 - 6, 18))
        self.c.itemconfig(self.size_item, text=f"{x1 - x0} × {y1 - y0}")

    def _release(self, e):
        if not self.start:
            return
        x0, y0, x1, y1 = self._box(e)
        self.start = None
        if x1 - x0 < 5 or y1 - y0 < 5:
            return  # click nhầm, chờ kéo lại
        region = {"left": self.mon["left"] + x0, "top": self.mon["top"] + y0,
                  "width": x1 - x0, "height": y1 - y0}
        self._finish(self.img.crop((x0, y0, x1, y1)), region)

    def _finish(self, img, region):
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()
        self.on_done(img, region)


# ----------------------------------------------------------------- trình chỉnh sửa
TOOLS = [
    ("arrow", "➜ Mũi tên"), ("rect", "▭ Khung"), ("ellipse", "◯ Elip"),
    ("pen", "✎ Bút"), ("highlight", "▮ Tô sáng"), ("text", "T Chữ"),
    ("blur", "▦ Làm mờ"), ("number", "① Số"), ("crop", "✂ Cắt"),
]


class Editor(tk.Toplevel):
    def __init__(self, app, img, path):
        super().__init__(app.root)
        self.app, self.img, self.path = app, img.convert("RGB"), path
        self.history, self.counter = [], 1
        self.color = "#ff2b2b"
        self.tool = tk.StringVar(value="arrow")
        self.width_var = tk.IntVar(value=4)
        self.start = None
        self.points = []
        self.scale = 1.0
        self.title(f"{APP_NAME} – Chỉnh sửa ảnh")
        self.attributes("-topmost", True)
        self.after(600, lambda: self.attributes("-topmost", False))

        bar = ttk.Frame(self, padding=4)
        bar.pack(side="top", fill="x")
        for key, label in TOOLS:
            tk.Radiobutton(bar, text=label, value=key, variable=self.tool, indicatoron=False,
                           padx=8, pady=3, font=("Segoe UI", 10)).pack(side="left", padx=1)
        self.color_btn = tk.Button(bar, text="  Màu  ", bg=self.color, fg="white",
                                   command=self.pick_color)
        self.color_btn.pack(side="left", padx=(10, 2))
        for c in ("#ff2b2b", "#ffd400", "#1e90ff", "#22c55e", "#000000"):
            tk.Button(bar, bg=c, width=2, relief="flat",
                      command=lambda c=c: self.set_color(c)).pack(side="left", padx=1)
        ttk.Label(bar, text="  Nét:").pack(side="left")
        ttk.Spinbox(bar, from_=1, to=40, width=4, textvariable=self.width_var).pack(side="left")

        bar2 = ttk.Frame(self, padding=(4, 0, 4, 4))
        bar2.pack(side="top", fill="x")
        ttk.Button(bar2, text="↶ Hoàn tác (Ctrl+Z)", command=self.undo).pack(side="left")
        ttk.Button(bar2, text="📋 Copy (Ctrl+C)", command=self.copy).pack(side="left", padx=2)
        ttk.Button(bar2, text="💾 Lưu (Ctrl+S)", command=self.save).pack(side="left", padx=2)
        ttk.Button(bar2, text="Lưu thành...", command=self.save_as).pack(side="left", padx=2)
        ttk.Button(bar2, text="📁 Mở thư mục", command=self.open_folder).pack(side="left", padx=2)
        ttk.Button(bar2, text="Copy & Đóng", command=self.copy_close).pack(side="right")

        self.canvas = tk.Canvas(self, highlightthickness=0, cursor="tcross", bg="#333")
        self.canvas.pack(side="top")
        self.status = ttk.Label(self, anchor="w", padding=(6, 2))
        self.status.pack(side="bottom", fill="x")

        self.canvas.bind("<ButtonPress-1>", self._press)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._release)
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-s>", lambda e: self.save())
        self.bind("<Control-c>", lambda e: self.copy())
        self.bind("<Escape>", lambda e: self.destroy())
        self.render()
        self.focus_force()

    # --- hiển thị
    def render(self):
        maxw = self.winfo_screenwidth() * 0.9
        maxh = self.winfo_screenheight() * 0.78
        self.scale = min(1.0, maxw / self.img.width, maxh / self.img.height)
        disp = self.img if self.scale == 1 else self.img.resize(
            (max(1, int(self.img.width * self.scale)), max(1, int(self.img.height * self.scale))),
            Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(disp)
        self.canvas.delete("all")
        self.canvas.config(width=disp.width, height=disp.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        where = f"Đã lưu: {self.path}" if self.path else "Chưa lưu"
        self.status.config(text=f"{self.img.width} × {self.img.height}px   •   {where}")

    def set_color(self, c):
        self.color = c
        self.color_btn.config(bg=c)

    def pick_color(self):
        c = colorchooser.askcolor(self.color, parent=self)[1]
        if c:
            self.set_color(c)

    def _img_xy(self, x, y):
        return x / self.scale, y / self.scale

    def _stroke(self):
        try:
            return max(1, int(self.width_var.get()))
        except (tk.TclError, ValueError):
            return 4

    # --- chuột
    def _press(self, e):
        self.start = (e.x, e.y)
        self.points = [(e.x, e.y)]
        t = self.tool.get()
        if t == "text":
            self.start = None
            s = simpledialog.askstring("Thêm chữ", "Nội dung:", parent=self)
            if s:
                self._commit(lambda im: self._draw_text(im, self._img_xy(e.x, e.y), s))
        elif t == "number":
            self.start = None
            self._commit(lambda im: self._draw_number(im, self._img_xy(e.x, e.y)))

    def _drag(self, e):
        if not self.start:
            return
        t = self.tool.get()
        x0, y0 = self.start
        w = max(1, self._stroke() * self.scale)
        if t == "pen":
            px, py = self.points[-1]
            self.canvas.create_line(px, py, e.x, e.y, fill=self.color, width=w,
                                    capstyle="round", tags="preview")
            self.points.append((e.x, e.y))
            return
        self.canvas.delete("preview")
        if t == "arrow":
            self.canvas.create_line(x0, y0, e.x, e.y, fill=self.color, width=w, arrow="last",
                                    arrowshape=(w * 4, w * 4, w * 1.8), tags="preview")
        elif t == "ellipse":
            self.canvas.create_oval(x0, y0, e.x, e.y, outline=self.color, width=w, tags="preview")
        elif t == "crop":
            self.canvas.create_rectangle(x0, y0, e.x, e.y, outline="white", dash=(6, 4),
                                         width=2, tags="preview")
        elif t in ("rect", "highlight", "blur"):
            self.canvas.create_rectangle(x0, y0, e.x, e.y, outline=self.color,
                                         width=w if t == "rect" else 2, tags="preview")

    def _release(self, e):
        if not self.start:
            return
        t = self.tool.get()
        p0 = self._img_xy(*self.start)
        p1 = self._img_xy(e.x, e.y)
        pts = [self._img_xy(*p) for p in self.points]
        self.start = None
        self.canvas.delete("preview")
        if t != "pen" and abs(p1[0] - p0[0]) < 3 and abs(p1[1] - p0[1]) < 3:
            return
        ops = {
            "pen": lambda im: self._draw_pen(im, pts),
            "arrow": lambda im: self._draw_arrow(im, p0, p1),
            "rect": lambda im: ImageDraw.Draw(im).rectangle(self._box(p0, p1),
                                                            outline=self.color, width=self._stroke()),
            "ellipse": lambda im: ImageDraw.Draw(im).ellipse(self._box(p0, p1),
                                                             outline=self.color, width=self._stroke()),
            "highlight": lambda im: self._draw_highlight(im, self._box(p0, p1)),
            "blur": lambda im: self._draw_blur(im, self._box(p0, p1)),
        }
        if t == "crop":
            box = self._box(p0, p1)
            self.history.append(self.img.copy())
            self.img = self.img.crop(box)
            self.render()
        elif t in ops:
            self._commit(ops[t])

    # --- vẽ lên ảnh thật (PIL)
    def _commit(self, fn):
        self.history.append(self.img.copy())
        result = fn(self.img)
        if isinstance(result, Image.Image):
            self.img = result
        self.render()

    def _box(self, p0, p1):
        x0, x1 = sorted((p0[0], p1[0]))
        y0, y1 = sorted((p0[1], p1[1]))
        return (max(0, int(x0)), max(0, int(y0)),
                min(self.img.width, int(x1)), min(self.img.height, int(y1)))

    def _draw_pen(self, im, pts):
        d = ImageDraw.Draw(im)
        w = self._stroke()
        if len(pts) > 1:
            d.line(pts, fill=self.color, width=w, joint="curve")
        for x, y in pts[:1] + pts[-1:]:
            d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=self.color)

    def _draw_arrow(self, im, p0, p1):
        d = ImageDraw.Draw(im)
        w = self._stroke()
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        head = max(12, w * 4)
        base = (p1[0] - head * 0.8 * math.cos(ang), p1[1] - head * 0.8 * math.sin(ang))
        d.line([p0, base], fill=self.color, width=w)
        left = (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45))
        right = (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))
        d.polygon([p1, left, right], fill=self.color)

    def _draw_highlight(self, im, box):
        overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        r, g, b = Image.new("RGB", (1, 1), self.color).getpixel((0, 0))
        ImageDraw.Draw(overlay).rectangle(box, fill=(r, g, b, 90))
        return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")

    def _draw_blur(self, im, box):
        x0, y0, x1, y1 = box
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        region = im.crop(box)
        block = max(6, min(region.size) // 8)
        small = region.resize((max(1, region.width // block), max(1, region.height // block)),
                              Image.BOX)
        im.paste(small.resize(region.size, Image.NEAREST), (x0, y0))

    def _draw_text(self, im, xy, text):
        font = load_font(max(16, self._stroke() * 5))
        d = ImageDraw.Draw(im)
        d.text(xy, text, fill=self.color, font=font,
               stroke_width=2, stroke_fill="white" if self.color != "#ffffff" else "black")

    def _draw_number(self, im, xy):
        r = max(14, self._stroke() * 3)
        x, y = xy
        d = ImageDraw.Draw(im)
        d.ellipse((x - r, y - r, x + r, y + r), fill=self.color, outline="white", width=2)
        d.text((x, y), str(self.counter), fill="white", font=load_font(int(r * 1.2)), anchor="mm")
        self.counter += 1

    # --- hành động
    def undo(self):
        if self.history:
            self.img = self.history.pop()
            self.render()

    def copy(self):
        ok = copy_image(self.img)
        self.app.toast("Đã copy ảnh vào clipboard ✔" if ok else "Copy clipboard thất bại")

    def copy_close(self):
        self.copy()
        self.destroy()

    def save(self):
        self.path = write_image(self.img, self.path or build_save_path(self.app.cfg), self.app.cfg)
        self.render()
        self.app.toast(f"Đã lưu: {Path(self.path).name}")

    def save_as(self):
        p = filedialog.asksaveasfilename(
            parent=self, defaultextension=".png",
            initialfile=Path(self.path).name if self.path else "anh.png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Tất cả", "*.*")])
        if p:
            self.path = write_image(self.img, p, self.app.cfg)
            self.render()

    def open_folder(self):
        folder = Path(self.path).parent if self.path else Path(self.app.cfg["save_dir"])
        folder.mkdir(parents=True, exist_ok=True)
        open_path(folder)


# ----------------------------------------------------------------- cài đặt
class SettingsDialog(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        cfg = app.cfg
        self.title(f"{APP_NAME} – Cài đặt")
        self.resizable(False, False)
        f = ttk.Frame(self, padding=14)
        f.pack(fill="both", expand=True)

        self.v = {
            "save_dir": tk.StringVar(value=cfg["save_dir"]),
            "filename_prefix": tk.StringVar(value=cfg["filename_prefix"]),
            "format": tk.StringVar(value=cfg["format"]),
            "jpg_quality": tk.IntVar(value=cfg["jpg_quality"]),
            "delay_seconds": tk.IntVar(value=cfg["delay_seconds"]),
            "subfolder_by_date": tk.BooleanVar(value=cfg["subfolder_by_date"]),
            "auto_save": tk.BooleanVar(value=cfg["auto_save"]),
            "copy_to_clipboard": tk.BooleanVar(value=cfg["copy_to_clipboard"]),
            "open_editor": tk.BooleanVar(value=cfg["open_editor"]),
            "autostart": tk.BooleanVar(value=cfg["autostart"]),
        }
        self.hk = {k: tk.StringVar(value=v) for k, v in cfg["hotkeys"].items()}

        r = 0
        ttk.Label(f, text="Thư mục lưu ảnh:").grid(row=r, column=0, sticky="w")
        ttk.Entry(f, textvariable=self.v["save_dir"], width=42).grid(row=r, column=1, sticky="we")
        ttk.Button(f, text="...", width=3, command=self.browse).grid(row=r, column=2, padx=2)
        r += 1
        ttk.Label(f, text="Tiền tố tên file:").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(f, textvariable=self.v["filename_prefix"], width=20).grid(row=r, column=1, sticky="w")
        r += 1
        ttk.Label(f, text="Định dạng:").grid(row=r, column=0, sticky="w")
        fm = ttk.Frame(f)
        fm.grid(row=r, column=1, sticky="w")
        ttk.Radiobutton(fm, text="PNG (nét)", value="png", variable=self.v["format"]).pack(side="left")
        ttk.Radiobutton(fm, text="JPG (nhẹ)", value="jpg", variable=self.v["format"]).pack(side="left", padx=8)
        ttk.Label(fm, text="Chất lượng JPG:").pack(side="left")
        ttk.Spinbox(fm, from_=30, to=100, width=4, textvariable=self.v["jpg_quality"]).pack(side="left")
        r += 1
        ttk.Label(f, text="Hẹn giờ (giây):").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Spinbox(f, from_=1, to=30, width=4, textvariable=self.v["delay_seconds"]).grid(row=r, column=1, sticky="w")
        r += 1
        for key, text in [("subfolder_by_date", "Tạo thư mục con theo tháng (VD: 2026-10)"),
                          ("auto_save", "Tự động lưu file ngay khi chụp"),
                          ("copy_to_clipboard", "Tự động copy vào clipboard (Ctrl+V để dán)"),
                          ("open_editor", "Mở trình chỉnh sửa sau khi chụp"),
                          ("autostart", "Khởi động cùng Windows")]:
            ttk.Checkbutton(f, text=text, variable=self.v[key]).grid(row=r, column=0, columnspan=3, sticky="w")
            r += 1

        ttk.Separator(f).grid(row=r, column=0, columnspan=3, sticky="we", pady=8)
        r += 1
        ttk.Label(f, text="Phím tắt  (VD: <ctrl>+<shift>+a, <alt>+s, <print_screen>; để trống = tắt)",
                  foreground="#555").grid(row=r, column=0, columnspan=3, sticky="w")
        r += 1
        for key, label in ACTION_LABELS.items():
            ttk.Label(f, text=label + ":").grid(row=r, column=0, sticky="w", pady=1)
            ttk.Entry(f, textvariable=self.hk.setdefault(key, tk.StringVar()), width=26).grid(
                row=r, column=1, sticky="w")
            r += 1

        btns = ttk.Frame(f)
        btns.grid(row=r, column=0, columnspan=3, sticky="e", pady=(12, 0))
        ttk.Button(btns, text="Khôi phục mặc định", command=self.reset).pack(side="left", padx=4)
        ttk.Button(btns, text="Hủy", command=self.destroy).pack(side="left", padx=4)
        ttk.Button(btns, text="Lưu", command=self.apply).pack(side="left")
        self.grab_set()

    def browse(self):
        d = filedialog.askdirectory(parent=self, initialdir=self.v["save_dir"].get())
        if d:
            self.v["save_dir"].set(d)

    def reset(self):
        for k, var in self.v.items():
            var.set(DEFAULT_CONFIG[k])
        for k, var in self.hk.items():
            var.set(DEFAULT_CONFIG["hotkeys"].get(k, ""))

    def apply(self):
        new = dict(self.app.cfg)
        try:
            for k, var in self.v.items():
                new[k] = var.get()
        except tk.TclError:
            messagebox.showerror(APP_NAME, "Giá trị số không hợp lệ.", parent=self)
            return
        new["hotkeys"] = {k: var.get().strip().lower() for k, var in self.hk.items()}
        old = self.app.cfg
        self.app.cfg = new
        if not self.app.start_hotkeys():
            self.app.cfg = old
            self.app.start_hotkeys()
            return
        try:
            set_autostart(new["autostart"])
        except Exception as e:
            messagebox.showwarning(APP_NAME, f"Không đặt được khởi động cùng Windows:\n{e}", parent=self)
        save_config(new)
        self.app.refresh_panel()
        self.destroy()


# ----------------------------------------------------------------- ứng dụng chính
class App:
    def __init__(self, start_hidden=False):
        self.cfg = load_config()
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} – Chụp màn hình")
        self.root.resizable(False, False)
        self.q = queue.Queue()
        self.hotkeys = None
        self.tray = None
        self.busy = False
        self.last_region = None
        self.panel_visible = not start_hidden

        self.build_panel()
        self.start_hotkeys()
        self.start_tray()
        if start_hidden and self.tray:
            self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(50, self.poll)

    # --- giao diện bảng điều khiển
    def build_panel(self):
        style = ttk.Style(self.root)
        style.configure("Big.TButton", font=("Segoe UI", 11), padding=(10, 8))
        f = ttk.Frame(self.root, padding=14)
        f.pack(fill="both", expand=True)
        ttk.Label(f, text="📷 SnapVF", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(f, text="Chụp màn hình nhanh – tự lưu, tự copy, chỉnh sửa ngay",
                  foreground="#555").pack(anchor="w", pady=(0, 10))
        self.btns = {}
        for key, label in ACTION_LABELS.items():
            b = ttk.Button(f, style="Big.TButton", width=40,
                           command=lambda k=key: self.post(k))
            b.pack(fill="x", pady=2)
            self.btns[key] = (b, label)
        bottom = ttk.Frame(f)
        bottom.pack(fill="x", pady=(10, 0))
        ttk.Button(bottom, text="📁 Mở thư mục ảnh", command=self.open_folder).pack(side="left")
        ttk.Button(bottom, text="⚙ Cài đặt", command=lambda: SettingsDialog(self)).pack(side="left", padx=4)
        ttk.Button(bottom, text="Thoát", command=self.quit).pack(side="right")
        self.info = ttk.Label(f, foreground="#555", wraplength=380)
        self.info.pack(anchor="w", pady=(8, 0))
        self.refresh_panel()

    def refresh_panel(self):
        for key, (b, label) in self.btns.items():
            if key == "delay":
                label = f"Chụp vùng sau {self.cfg['delay_seconds']} giây"
            b.config(text=f"{label}    [{pretty_hotkey(self.cfg['hotkeys'].get(key, ''))}]")
        tray = "Đóng cửa sổ này app vẫn chạy dưới khay hệ thống (góc phải thanh Taskbar)." \
            if self.tray else ""
        self.info.config(text=f"Ảnh lưu tại: {self.cfg['save_dir']}\n{tray}")

    # --- phím tắt / khay hệ thống (chạy ở luồng khác -> đẩy vào hàng đợi)
    def post(self, action):
        self.q.put(action)

    def poll(self):
        try:
            while True:
                self.dispatch(self.q.get_nowait())
        except queue.Empty:
            pass
        self.root.after(50, self.poll)

    def start_hotkeys(self):
        if self.hotkeys:
            self.hotkeys.stop()
            self.hotkeys = None
        mapping = {}
        for action, combo in self.cfg["hotkeys"].items():
            if combo:
                mapping[combo] = (lambda a=action: self.post(a))
        try:
            self.hotkeys = keyboard.GlobalHotKeys(mapping)
            self.hotkeys.start()
            return True
        except Exception as e:
            messagebox.showerror(APP_NAME, f"Phím tắt không hợp lệ: {e}")
            return False

    def start_tray(self):
        if not pystray:
            return
        def item(text, action, default=False):
            return pystray.MenuItem(text, lambda icon, it: self.post(action), default=default)
        menu = pystray.Menu(
            item("Chụp vùng chọn", "region", default=True),
            item("Chụp toàn màn hình", "full"),
            item("Chụp cửa sổ đang mở", "window"),
            item("Chụp lại vùng trước", "last"),
            item("Chụp vùng sau X giây", "delay"),
            pystray.Menu.SEPARATOR,
            item("Mở bảng điều khiển", "show"),
            item("Mở thư mục ảnh", "open_folder"),
            item("Cài đặt", "settings"),
            pystray.Menu.SEPARATOR,
            item("Thoát", "quit"),
        )
        try:
            self.tray = pystray.Icon(APP_NAME, make_tray_icon(), "SnapVF – Chụp màn hình", menu)
            self.tray.run_detached()
        except Exception as e:
            print("Không tạo được icon khay:", e)
            self.tray = None

    def dispatch(self, action):
        if action in ("region", "full", "window", "last"):
            self.begin(action, 0)
        elif action == "delay":
            self.begin("region", int(self.cfg["delay_seconds"]))
        elif action == "show":
            self.show_panel()
        elif action == "open_folder":
            self.open_folder()
        elif action == "settings":
            self.show_panel()
            SettingsDialog(self)
        elif action == "quit":
            self.quit()

    # --- quy trình chụp
    def begin(self, mode, delay):
        if self.busy:
            return
        self.busy = True
        self.panel_visible = self.root.state() != "withdrawn"
        self.root.withdraw()  # ẩn bảng điều khiển để không lọt vào ảnh
        if delay > 0:
            self.countdown(delay, lambda: self.root.after(200, lambda: self.capture(mode)))
        else:
            self.root.after(250, lambda: self.capture(mode))

    def capture(self, mode):
        try:
            if mode == "full":
                self.finish(grab()[0])
            elif mode == "window":
                rect = foreground_window_rect()
                self.finish(grab(rect)[0])
            elif mode == "last" and self.last_region:
                self.finish(grab(self.last_region)[0])
            else:
                img, mon = grab()
                RegionSelector(self, img, mon, self.on_region)
        except Exception as e:
            self.busy = False
            self.restore_panel()
            messagebox.showerror(APP_NAME, f"Lỗi khi chụp: {e}")

    def on_region(self, img, region):
        if region:
            self.last_region = region
        if img is None:
            self.busy = False
            self.restore_panel()
            return
        self.finish(img)

    def finish(self, img):
        self.busy = False
        cfg = self.cfg
        path = None
        msgs = []
        try:
            if cfg["auto_save"]:
                path = write_image(img, build_save_path(cfg), cfg)
                msgs.append(f"Đã lưu {path.name}")
        except Exception as e:
            messagebox.showerror(APP_NAME, f"Không lưu được ảnh: {e}")
        if cfg["copy_to_clipboard"] and copy_image(img):
            msgs.append("đã copy (Ctrl+V để dán)")
        if cfg["open_editor"]:
            Editor(self, img, path)
        elif msgs:
            self.toast(" – ".join(msgs))
        self.restore_panel()

    def restore_panel(self):
        if self.panel_visible or not self.tray:
            self.root.deiconify()

    # --- tiện ích UI
    def _popup(self, text, font, ms=None):
        t = tk.Toplevel(self.root)
        t.overrideredirect(True)
        t.attributes("-topmost", True)
        lbl = tk.Label(t, text=text, bg="#1f2937", fg="white", padx=16, pady=10, font=font)
        lbl.pack()
        t.update_idletasks()
        x = self.root.winfo_screenwidth() - t.winfo_reqwidth() - 24
        y = self.root.winfo_screenheight() - t.winfo_reqheight() - 70
        t.geometry(f"+{x}+{y}")
        if ms:
            t.after(ms, t.destroy)
        return t, lbl

    def toast(self, text, ms=2500):
        self._popup(text, ("Segoe UI", 10), ms)

    def countdown(self, n, then):
        t, lbl = self._popup(str(n), ("Segoe UI", 28, "bold"))

        def tick(k):
            if k <= 0:
                t.destroy()
                then()
                return
            lbl.config(text=f"Chụp sau {k}s")
            t.after(1000, tick, k - 1)
        tick(n)

    def open_folder(self):
        folder = Path(os.path.expandvars(os.path.expanduser(self.cfg["save_dir"])))
        folder.mkdir(parents=True, exist_ok=True)
        open_path(folder)

    def show_panel(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def on_close(self):
        if self.tray:
            self.root.withdraw()
            self.toast("SnapVF vẫn chạy dưới khay hệ thống")
        else:
            self.quit()

    def quit(self):
        if self.hotkeys:
            self.hotkeys.stop()
        if self.tray:
            self.tray.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def ensure_single_instance():
    if not IS_WIN:
        return True
    global _mutex
    _mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "SnapVF_single_instance_mutex")
    return ctypes.windll.kernel32.GetLastError() != 183  # ERROR_ALREADY_EXISTS


if __name__ == "__main__":
    if not ensure_single_instance():
        r = tk.Tk()
        r.withdraw()
        messagebox.showinfo(APP_NAME, "SnapVF đang chạy rồi (xem biểu tượng ở khay hệ thống).")
        sys.exit(0)
    App(start_hidden="--tray" in sys.argv).run()
