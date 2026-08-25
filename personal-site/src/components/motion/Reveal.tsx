"use client";

import type { ReactNode } from "react";
import { motion, useReducedMotion } from "motion/react";

type Direction = "up" | "left" | "right";

const offsets: Record<Direction, { x: number; y: number }> = {
  up: { x: 0, y: 24 },
  left: { x: -24, y: 0 },
  right: { x: 24, y: 0 },
};

export function Reveal({
  children,
  delay = 0,
  direction = "up",
  className,
}: {
  children: ReactNode;
  delay?: number;
  direction?: Direction;
  className?: string;
}) {
  const shouldReduceMotion = useReducedMotion();
  const offset = offsets[direction];

  return (
    <motion.div
      className={className}
      initial={
        shouldReduceMotion
          ? { opacity: 0 }
          : { opacity: 0, x: offset.x, y: offset.y }
      }
      whileInView={shouldReduceMotion ? { opacity: 1 } : { opacity: 1, x: 0, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}
