type GlowBlobProps = {
  color: "accent" | "accent-2" | "accent-3";
  className?: string;
  delay?: string;
};

const colorVar: Record<GlowBlobProps["color"], string> = {
  accent: "var(--accent)",
  "accent-2": "var(--accent-2)",
  "accent-3": "var(--accent-3)",
};

export function GlowBlob({ color, className = "", delay = "0s" }: GlowBlobProps) {
  return (
    <div
      aria-hidden="true"
      className={`animate-blob-float pointer-events-none absolute rounded-full blur-3xl ${className}`}
      style={{
        background: `radial-gradient(circle at center, ${colorVar[color]}, transparent 70%)`,
        opacity: "var(--glow-opacity)",
        animationDelay: delay,
      }}
    />
  );
}
