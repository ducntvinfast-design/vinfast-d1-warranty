import { Code2, Link as LinkIcon, Mail } from "lucide-react";
import { profile } from "@/data/profile";
import { Reveal } from "@/components/motion/Reveal";
import { GlowBlob } from "@/components/motion/GlowBlob";

const links = [
  { href: `mailto:${profile.social.email}`, label: profile.social.email, icon: Mail },
  { href: profile.social.github, label: "GitHub", icon: Code2 },
  { href: profile.social.linkedin, label: "LinkedIn", icon: LinkIcon },
];

export function Contact() {
  return (
    <section id="contact" className="scroll-mt-20 py-16 sm:py-24">
      <Reveal>
        <div className="relative isolate overflow-hidden rounded-3xl border border-border-color bg-surface/40 px-8 py-16 text-center backdrop-blur-xl sm:py-24">
          <GlowBlob color="accent-2" className="-top-24 left-1/4 h-72 w-72" />
          <GlowBlob color="accent-3" className="-bottom-24 right-1/4 h-72 w-72" delay="6s" />

          <p className="font-mono text-xs uppercase tracking-widest text-accent-2">
            Liên hệ
          </p>
          <h2 className="text-gradient-brand mt-2 font-display text-3xl font-semibold tracking-tight sm:text-5xl">
            Cùng trao đổi nhé
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-foreground-muted">
            Nếu anh muốn trao đổi công việc, hợp tác dự án, hoặc chỉ đơn giản là
            nói chuyện, hãy liên hệ qua các kênh dưới đây.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            {links.map(({ href, label, icon: Icon }) => (
              <a
                key={label}
                href={href}
                className="flex items-center gap-2 rounded-full border border-border-color bg-white/5 px-4 py-2 text-sm transition-all hover:border-border-hover hover:shadow-[0_0_30px_-10px_var(--accent)]"
              >
                <Icon size={16} />
                {label}
              </a>
            ))}
          </div>
        </div>
      </Reveal>
    </section>
  );
}
