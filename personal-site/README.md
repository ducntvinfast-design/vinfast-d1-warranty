# nguyentaiduc.com — Website thương hiệu cá nhân

Website cá nhân (portfolio + blog) xây dựng bằng Next.js (App Router), TypeScript,
và Tailwind CSS. Đây là một dự án Next.js độc lập, nằm trong thư mục con
`personal-site/` của repo — không liên quan đến, và không ảnh hưởng tới, file
`index.html` ở thư mục gốc của repo.

## Nội dung hiện là placeholder

Toàn bộ thông tin cá nhân, kinh nghiệm, dự án và bài blog trong dự án này hiện là
**nội dung mẫu (placeholder)**. Trước khi đưa site lên `nguyentaiduc.com`, hãy thay
bằng thông tin thật:

- **Thông tin cá nhân / portfolio**: chỉnh sửa file [`src/data/profile.ts`](./src/data/profile.ts)
  — đây là nơi duy nhất cần sửa để cập nhật tên, tagline, giới thiệu, kỹ năng,
  kinh nghiệm làm việc, dự án, và thông tin liên hệ (email, GitHub, LinkedIn).
- **Bài blog**: thêm/sửa/xoá file `.mdx` trong [`content/blog/`](./content/blog).
  Mỗi file cần có frontmatter dạng:

  ```md
  ---
  title: "Tiêu đề bài viết"
  date: "2026-01-01"
  excerpt: "Mô tả ngắn hiển thị ở trang danh sách blog."
  tags: ["tag1", "tag2"]
  ---

  Nội dung bài viết ở đây, viết bằng Markdown/MDX.
  ```

## Chạy dự án

```bash
npm install
npm run dev
```

Mở [http://localhost:3000](http://localhost:3000) để xem site.

Kiểm tra build production trước khi deploy:

```bash
npm run build
```

## Deploy

Khi đã mua domain `nguyentaiduc.com`, cách deploy đơn giản nhất là dùng
[Vercel](https://vercel.com): kết nối repo, đặt **Root Directory** của project là
`personal-site/`, Vercel sẽ tự nhận diện Next.js. Sau đó gắn domain
`nguyentaiduc.com` qua phần Domains của project trên Vercel.
