import Link from "next/link";
import { profile } from "@/data/profile";

export function Hero() {
  return (
    <section className="flex flex-col items-start gap-6 py-20 sm:py-28">
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-accent/10 text-2xl font-semibold text-accent">
        {profile.avatarInitials}
      </div>
      <div>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
          {profile.name}
        </h1>
        <p className="mt-2 text-lg text-foreground/70">{profile.tagline}</p>
      </div>
      <p className="max-w-2xl text-foreground/80">{profile.bio[0]}</p>
      <div className="flex gap-3 text-sm font-medium">
        <Link
          href="#projects"
          className="rounded-full bg-accent px-5 py-2.5 text-white transition-opacity hover:opacity-90"
        >
          Xem dự án
        </Link>
        <Link
          href="/blog"
          className="rounded-full border border-border-color px-5 py-2.5 transition-colors hover:border-foreground/30"
        >
          Đọc blog
        </Link>
      </div>
    </section>
  );
}
