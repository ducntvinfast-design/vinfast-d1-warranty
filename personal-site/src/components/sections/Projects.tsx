import { ExternalLink } from "lucide-react";
import { projects } from "@/data/profile";
import { Reveal } from "@/components/motion/Reveal";

export function Projects() {
  return (
    <section id="projects" className="scroll-mt-20 py-16 sm:py-24">
      <Reveal>
        <p className="font-mono text-xs uppercase tracking-widest text-accent-2">
          Dự án
        </p>
        <h2 className="mt-2 font-display text-3xl font-semibold tracking-tight sm:text-4xl">
          Sản phẩm nổi bật
        </h2>
      </Reveal>

      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        {projects.map((project, index) => (
          <Reveal key={project.name} delay={index * 0.1}>
            <a
              href={project.link ?? "#"}
              className="group block rounded-2xl border border-border-color bg-surface/40 p-6 backdrop-blur-xl transition-all hover:border-border-hover hover:shadow-[0_0_40px_-8px_var(--accent)]"
            >
              <div className="flex items-start justify-between gap-2">
                <h3 className="font-display font-medium">{project.name}</h3>
                <ExternalLink
                  size={16}
                  className="mt-1 shrink-0 text-foreground-muted transition-colors group-hover:text-accent-2"
                />
              </div>
              <p className="mt-2 text-sm text-foreground-muted">
                {project.description}
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span
                    key={tag}
                    className="rounded-full border border-border-color px-2.5 py-1 font-mono text-xs text-foreground-muted"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </a>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
