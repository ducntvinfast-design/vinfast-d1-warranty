// Nguồn duy nhất cho thông tin cá nhân — chỉnh sửa file này để cập nhật nội dung site.
// TODO: thay toàn bộ nội dung placeholder dưới đây bằng thông tin thật của anh.

export const profile = {
  name: "Nguyễn Tài Đức",
  tagline: "Kỹ sư phần mềm",
  location: "Việt Nam",
  bio: [
    "Xin chào, mình là Đức. Đây là trang cá nhân nơi mình giới thiệu công việc, chia sẻ những gì mình học được, và ghi lại vài suy nghĩ dọc đường.",
    "Nội dung trên trang này hiện là placeholder — sẽ được thay bằng thông tin thật trong thời gian tới.",
  ],
  avatarInitials: "TD",
  social: {
    email: "contact@nguyentaiduc.com",
    github: "https://github.com/",
    linkedin: "https://www.linkedin.com/",
  },
} as const;

export type Skill = {
  category: string;
  items: string[];
};

export const skills: Skill[] = [
  { category: "Ngôn ngữ", items: ["TypeScript", "JavaScript", "Python"] },
  { category: "Frontend", items: ["React", "Next.js", "Tailwind CSS"] },
  { category: "Backend", items: ["Node.js", "PostgreSQL", "REST API"] },
  { category: "Công cụ", items: ["Git", "Docker", "Linux"] },
];

export type Experience = {
  role: string;
  organization: string;
  period: string;
  description: string;
};

export const experience: Experience[] = [
  {
    role: "Vị trí công việc (placeholder)",
    organization: "Tên công ty (placeholder)",
    period: "20XX — Hiện tại",
    description:
      "Mô tả ngắn về công việc, trách nhiệm chính và những gì đã đóng góp ở vị trí này.",
  },
  {
    role: "Vị trí trước đó (placeholder)",
    organization: "Tên công ty trước đó (placeholder)",
    period: "20XX — 20XX",
    description:
      "Mô tả ngắn về công việc trước đó và những kinh nghiệm tích lũy được.",
  },
];

export type Project = {
  name: string;
  description: string;
  tags: string[];
  link?: string;
};

export const projects: Project[] = [
  {
    name: "Tên dự án 1 (placeholder)",
    description:
      "Mô tả ngắn gọn về dự án: vấn đề gì được giải quyết, công nghệ sử dụng, kết quả đạt được.",
    tags: ["Next.js", "TypeScript"],
    link: "#",
  },
  {
    name: "Tên dự án 2 (placeholder)",
    description:
      "Mô tả ngắn gọn về dự án khác, có thể là sản phẩm cá nhân hoặc đóng góp mã nguồn mở.",
    tags: ["Node.js", "PostgreSQL"],
    link: "#",
  },
];
