import { profile } from "@/data/profile";

export function Footer() {
  return (
    <footer className="border-t border-border-color">
      <div className="mx-auto max-w-4xl px-6 py-8 text-sm text-foreground/60">
        © {new Date().getFullYear()} {profile.name}. Được xây dựng với Next.js.
      </div>
    </footer>
  );
}
