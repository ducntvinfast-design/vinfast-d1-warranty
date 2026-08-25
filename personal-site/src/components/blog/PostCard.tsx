import Link from "next/link";
import type { PostMeta } from "@/lib/posts";

function formatDate(date: string) {
  return new Date(date).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function PostCard({ post }: { post: PostMeta }) {
  return (
    <Link
      href={`/blog/${post.slug}`}
      className="group block rounded-2xl border border-border-color bg-surface/40 p-6 backdrop-blur-xl transition-all hover:border-border-hover hover:shadow-[0_0_40px_-8px_var(--accent)]"
    >
      <div className="flex items-center gap-3 font-mono text-xs text-foreground-muted">
        <time dateTime={post.date}>{formatDate(post.date)}</time>
        <span>·</span>
        <span>{post.readingTime}</span>
      </div>
      <h3 className="mt-2 font-display font-medium transition-colors group-hover:text-accent-2">
        {post.title}
      </h3>
      <p className="mt-2 text-sm text-foreground-muted">{post.excerpt}</p>
      {post.tags.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {post.tags.map((tag) => (
            <span
              key={tag}
              className="rounded-full border border-border-color px-2.5 py-1 font-mono text-xs text-foreground-muted"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
