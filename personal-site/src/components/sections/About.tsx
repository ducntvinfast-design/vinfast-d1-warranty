import { profile, skills } from "@/data/profile";
import { Reveal } from "@/components/motion/Reveal";

export function About() {
  return (
    <section id="about" className="scroll-mt-20 py-16 sm:py-24">
      <Reveal>
        <p className="font-mono text-xs uppercase tracking-widest text-accent-2">
          Giới thiệu
        </p>
        <h2 className="mt-2 font-display text-3xl font-semibold tracking-tight sm:text-4xl">
          Về mình
        </h2>
      </Reveal>

      <Reveal delay={0.1}>
        <div className="mt-8 rounded-3xl border border-border-color bg-surface/40 p-8 backdrop-blur-xl">
          <div className="max-w-2xl space-y-3 text-foreground-muted">
            {profile.bio.slice(1).map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
            <p className="text-sm text-foreground-muted/70">{profile.location}</p>
          </div>

          <div className="mt-8 grid gap-6 sm:grid-cols-2">
            {skills.map((group) => (
              <div key={group.category}>
                <h3 className="text-sm font-medium text-foreground-muted">
                  {group.category}
                </h3>
                <ul className="mt-2 flex flex-wrap gap-2">
                  {group.items.map((item) => (
                    <li
                      key={item}
                      className="rounded-full border border-border-color px-3 py-1 text-sm text-foreground transition-colors hover:border-accent/40"
                    >
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </Reveal>
    </section>
  );
}
