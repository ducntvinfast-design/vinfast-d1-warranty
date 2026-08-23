import Link from "next/link";
import { profile } from "@/data/profile";
import { ThemeToggle } from "./ThemeToggle";

const navLinks = [
  { href: "/#about", label: "Giới thiệu" },
  { href: "/#experience", label: "Kinh nghiệm" },
  { href: "/#projects", label: "Dự án" },
  { href: "/blog", label: "Blog" },
  { href: "/#contact", label: "Liên hệ" },
];

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-border-color bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
        <Link href="/" className="font-semibold tracking-tight">
          {profile.name}
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-foreground/70 sm:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="transition-colors hover:text-foreground"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <nav className="flex items-center gap-4 text-sm text-foreground/70 sm:hidden">
            <Link href="/blog" className="transition-colors hover:text-foreground">
              Blog
            </Link>
          </nav>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
