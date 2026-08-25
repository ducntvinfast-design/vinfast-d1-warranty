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
    <header className="sticky top-0 z-50 border-b border-border-color bg-background/60 backdrop-blur-xl">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2 font-display font-semibold tracking-tight">
          <span className="h-2 w-2 rounded-full bg-gradient-brand" />
          {profile.name}
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-foreground-muted sm:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="group relative py-1 transition-colors hover:text-foreground"
            >
              {link.label}
              <span className="absolute inset-x-0 -bottom-0.5 h-px origin-left scale-x-0 bg-gradient-brand transition-transform duration-300 group-hover:scale-x-100" />
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <nav className="flex items-center gap-4 text-sm text-foreground-muted sm:hidden">
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
