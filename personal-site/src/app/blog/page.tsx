import type { Metadata } from "next";
import { getAllPosts } from "@/lib/posts";
import { PostCard } from "@/components/blog/PostCard";
import { Reveal } from "@/components/motion/Reveal";

export const metadata: Metadata = {
  title: "Blog",
};

export default function BlogIndexPage() {
  const posts = getAllPosts();

  return (
    <div className="mx-auto max-w-5xl px-6 py-16 sm:py-24">
      <Reveal>
        <p className="font-mono text-xs uppercase tracking-widest text-accent-2">
          Blog
        </p>
        <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight sm:text-5xl">
          Ghi chép
        </h1>
        <p className="mt-3 max-w-xl text-foreground-muted">
          Ghi chép về công việc, kỹ thuật, và những suy nghĩ dọc đường.
        </p>
      </Reveal>
      <div className="mt-10 space-y-4">
        {posts.map((post, index) => (
          <Reveal key={post.slug} delay={index * 0.08}>
            <PostCard post={post} />
          </Reveal>
        ))}
      </div>
    </div>
  );
}
