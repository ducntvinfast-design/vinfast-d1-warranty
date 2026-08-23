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
      className="group block rounded-xl border border-border-color p-5 transition-colors hover:border-foreground/30"
    >
      <div className="flex items-center gap-3 text-sm text-foreground/50">
        <time dateTime={post.date}>{formatDate(post.date)}</time>
        <span>·</span>
        <span>{post.readingTime}</span>
      </div>
      <h3 className="mt-2 font-medium group-hover:text-accent">
        {post.title}
      </h3>
      <p className="mt-2 text-sm text-foreground/70">{post.excerpt}</p>
      {post.tags.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {post.tags.map((tag) => (
            <span
              key={tag}
              className="rounded-full bg-surface px-2.5 py-1 text-xs text-foreground/60"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
