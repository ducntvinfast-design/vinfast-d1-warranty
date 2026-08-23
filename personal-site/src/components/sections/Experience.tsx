import { experience } from "@/data/profile";

export function Experience() {
  return (
    <section
      id="experience"
      className="scroll-mt-20 border-t border-border-color py-16"
    >
      <h2 className="text-xl font-semibold tracking-tight">Kinh nghiệm</h2>
      <div className="mt-6 space-y-8">
        {experience.map((item) => (
          <div key={`${item.organization}-${item.role}`}>
            <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
              <h3 className="font-medium">
                {item.role} · {item.organization}
              </h3>
              <span className="text-sm text-foreground/50">{item.period}</span>
            </div>
            <p className="mt-1 text-foreground/70">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
