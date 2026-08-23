import { Code2, Link as LinkIcon, Mail } from "lucide-react";
import { profile } from "@/data/profile";

const links = [
  { href: `mailto:${profile.social.email}`, label: profile.social.email, icon: Mail },
  { href: profile.social.github, label: "GitHub", icon: Code2 },
  { href: profile.social.linkedin, label: "LinkedIn", icon: LinkIcon },
];

export function Contact() {
  return (
    <section
      id="contact"
      className="scroll-mt-20 border-t border-border-color py-16"
    >
      <h2 className="text-xl font-semibold tracking-tight">Liên hệ</h2>
      <p className="mt-3 max-w-xl text-foreground/70">
        Nếu anh muốn trao đổi công việc, hợp tác dự án, hoặc chỉ đơn giản là nói
        chuyện, hãy liên hệ qua các kênh dưới đây.
      </p>
      <div className="mt-6 flex flex-wrap gap-3">
        {links.map(({ href, label, icon: Icon }) => (
          <a
            key={label}
            href={href}
            className="flex items-center gap-2 rounded-full border border-border-color px-4 py-2 text-sm transition-colors hover:border-foreground/30"
          >
            <Icon size={16} />
            {label}
          </a>
        ))}
      </div>
    </section>
  );
}
