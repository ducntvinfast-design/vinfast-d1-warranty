import { profile, skills } from "@/data/profile";

export function About() {
  return (
    <section id="about" className="scroll-mt-20 border-t border-border-color py-16">
      <h2 className="text-xl font-semibold tracking-tight">Giới thiệu</h2>
      <div className="mt-4 max-w-2xl space-y-3 text-foreground/80">
        {profile.bio.slice(1).map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
        <p className="text-sm text-foreground/60">{profile.location}</p>
      </div>

      <div className="mt-8 grid gap-6 sm:grid-cols-2">
        {skills.map((group) => (
          <div key={group.category}>
            <h3 className="text-sm font-medium text-foreground/60">
              {group.category}
            </h3>
            <ul className="mt-2 flex flex-wrap gap-2">
              {group.items.map((item) => (
                <li
                  key={item}
                  className="rounded-full bg-surface px-3 py-1 text-sm text-foreground/80"
                >
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
