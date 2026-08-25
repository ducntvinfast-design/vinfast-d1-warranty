"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "motion/react";
import { profile } from "@/data/profile";
import { GlowBlob } from "@/components/motion/GlowBlob";

const container = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12, delayChildren: 0.1 } },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] as const } },
};

export function Hero() {
  const shouldReduceMotion = useReducedMotion();
  const initial = shouldReduceMotion ? "visible" : "hidden";

  return (
    <section className="relative isolate flex flex-col items-start gap-8 overflow-hidden py-24 sm:py-32">
      <GlowBlob color="accent" className="-top-32 -left-24 h-96 w-96" />
      <GlowBlob color="accent-2" className="-right-24 top-10 h-80 w-80" delay="4s" />
      <GlowBlob color="accent-3" className="bottom-0 left-1/3 h-72 w-72" delay="8s" />

      <motion.div
        variants={container}
        initial={initial}
        animate="visible"
        className="flex flex-col items-start gap-6"
      >
        <motion.div
          variants={item}
          className="flex h-20 w-20 items-center justify-center rounded-full bg-gradient-brand p-[2px]"
        >
          <div className="flex h-full w-full items-center justify-center rounded-full bg-background text-xl font-display font-semibold text-foreground">
            {profile.avatarInitials}
          </div>
        </motion.div>

        <motion.div variants={item}>
          <h1 className="text-gradient-brand font-display text-5xl font-bold leading-[0.95] tracking-tighter sm:text-7xl lg:text-8xl">
            {profile.name}
          </h1>
          <p className="mt-4 text-xl text-foreground-muted sm:text-2xl">
            {profile.tagline}
          </p>
        </motion.div>

        <motion.p variants={item} className="max-w-2xl text-foreground-muted">
          {profile.bio[0]}
        </motion.p>

        <motion.div variants={item} className="flex flex-wrap gap-3 text-sm font-medium">
          <Link
            href="#projects"
            className="rounded-full bg-gradient-brand px-6 py-3 text-white shadow-[0_0_40px_-8px_var(--accent)] transition-transform hover:scale-[1.03]"
          >
            Xem dự án
          </Link>
          <Link
            href="/blog"
            className="rounded-full border border-border-color bg-white/5 px-6 py-3 backdrop-blur-xl transition-all hover:border-border-hover hover:shadow-[0_0_30px_-10px_var(--accent-2)]"
          >
            Đọc blog
          </Link>
        </motion.div>
      </motion.div>
    </section>
  );
}
