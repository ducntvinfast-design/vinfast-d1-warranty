import { Hero } from "@/components/sections/Hero";
import { About } from "@/components/sections/About";
import { Experience } from "@/components/sections/Experience";
import { Projects } from "@/components/sections/Projects";
import { Contact } from "@/components/sections/Contact";

export default function Home() {
  return (
    <div className="mx-auto max-w-5xl px-6">
      <Hero />
      <About />
      <Experience />
      <Projects />
      <Contact />
    </div>
  );
}
