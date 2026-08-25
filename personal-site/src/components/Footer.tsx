import { profile } from "@/data/profile";

export function Footer() {
  return (
    <footer className="border-t border-border-color">
      <div className="mx-auto max-w-5xl px-6 py-10 font-mono text-xs text-foreground-muted">
        © {new Date().getFullYear()} {profile.name}. Built with Next.js.
      </div>
    </footer>
  );
}
