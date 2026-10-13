# SnapVF – Phần mềm chụp màn hình

## Cài đặt (Windows)
1. Cài **Python 3.10+** từ https://www.python.org/downloads/ (nhớ tick **"Add Python to PATH"**).
2. Giải nén thư mục `SnapVF`, nhấp đúp **`build_exe.bat`** → chờ 1–2 phút.
3. File chạy nằm ở `dist\SnapVF.exe` → copy đi đâu cũng được, nhấp đúp để mở.
   *(Muốn chạy thử không cần đóng gói: nhấp đúp `run.bat`.)*

## Phím tắt mặc định
| Phím | Chức năng |
|---|---|
| `Ctrl+Shift+A` | Chụp vùng chọn (kéo chuột) |
| `Ctrl+Shift+F` | Chụp toàn màn hình |
| `Ctrl+Shift+W` | Chụp cửa sổ đang mở |
| `Ctrl+Shift+R` | Chụp lại đúng vùng lần trước |
| `Ctrl+Shift+D` | Hẹn giờ 3 giây rồi chọn vùng (để chụp menu xổ xuống) |

Khi chọn vùng: **click đúp** = lấy cả màn hình, **Esc / chuột phải** = hủy.

## Sau khi chụp
- Ảnh **tự lưu** vào `Pictures\SnapVF\<năm-tháng>\Anh_<ngày>_<giờ>.png`
- Ảnh **tự copy** → mở Zalo / Word / Excel / Email bấm **Ctrl+V** là dán.
- Cửa sổ chỉnh sửa: Mũi tên, Khung, Elip, Bút, Tô sáng, Chữ (gõ tiếng Việt), Làm mờ (che biển số, SĐT…),
  Đánh số ①②③, Cắt ảnh. `Ctrl+Z` hoàn tác, `Ctrl+S` lưu, `Ctrl+C` copy, `Esc` đóng.

## Tùy chỉnh (nút ⚙ Cài đặt hoặc chuột phải icon dưới khay)
Đổi thư mục lưu, tên file, PNG/JPG, số giây hẹn giờ, bật/tắt tự lưu – tự copy – mở trình sửa,
**khởi động cùng Windows**, và đổi toàn bộ phím tắt (VD: `<print_screen>`, `<alt>+s`, `<ctrl>+<alt>+1`).

Đóng cửa sổ chính thì app vẫn chạy ẩn dưới khay hệ thống (góc phải thanh Taskbar).
