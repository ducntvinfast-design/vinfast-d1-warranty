import { ExternalLink } from "lucide-react";
import { projects } from "@/data/profile";

export function Projects() {
  return (
    <section
      id="projects"
      className="scroll-mt-20 border-t border-border-color py-16"
    >
      <h2 className="text-xl font-semibold tracking-tight">Dự án</h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {projects.map((project) => (
          <a
            key={project.name}
            href={project.link ?? "#"}
            className="group rounded-xl border border-border-color p-5 transition-colors hover:border-foreground/30"
          >
            <div className="flex items-start justify-between gap-2">
              <h3 className="font-medium">{project.name}</h3>
              <ExternalLink
                size={16}
                className="mt-1 shrink-0 text-foreground/40 transition-colors group-hover:text-foreground/70"
              />
            </div>
            <p className="mt-2 text-sm text-foreground/70">
              {project.description}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {project.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-surface px-2.5 py-1 text-xs text-foreground/60"
                >
                  {tag}
                </span>
              ))}
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}
