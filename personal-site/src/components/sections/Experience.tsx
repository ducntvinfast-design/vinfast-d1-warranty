import { experience } from "@/data/profile";
import { Reveal } from "@/components/motion/Reveal";

export function Experience() {
  return (
    <section id="experience" className="scroll-mt-20 py-16 sm:py-24">
      <Reveal>
        <p className="font-mono text-xs uppercase tracking-widest text-accent-2">
          Kinh nghiệm
        </p>
        <h2 className="mt-2 font-display text-3xl font-semibold tracking-tight sm:text-4xl">
          Chặng đường
        </h2>
      </Reveal>

      <div className="relative mt-10 space-y-10 pl-8">
        <div className="absolute top-1 bottom-1 left-[5px] w-px bg-gradient-to-b from-accent/60 to-transparent" />
        {experience.map((item, index) => (
          <Reveal key={`${item.organization}-${item.role}`} delay={index * 0.1} direction="left">
            <div className="relative">
              <span className="absolute -left-8 top-1.5 h-2.5 w-2.5 rounded-full bg-accent shadow-[0_0_12px_2px_var(--accent)]" />
              <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
                <h3 className="font-medium">
                  {item.role} · {item.organization}
                </h3>
                <span className="font-mono text-sm text-foreground-muted">
                  {item.period}
                </span>
              </div>
              <p className="mt-1 text-foreground-muted">{item.description}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
