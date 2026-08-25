import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { getAllSlugs, getPostBySlug } from "@/lib/posts";
import { PostBody } from "@/components/blog/PostBody";
import { Reveal } from "@/components/motion/Reveal";

function formatDate(date: string) {
  return new Date(date).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: PageProps<"/blog/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  try {
    const post = getPostBySlug(slug);
    return { title: post.title, description: post.excerpt };
  } catch {
    return {};
  }
}

export default async function BlogPostPage({
  params,
}: PageProps<"/blog/[slug]">) {
  const { slug } = await params;

  let post;
  try {
    post = getPostBySlug(slug);
  } catch {
    notFound();
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-16 sm:py-24">
      <Link
        href="/blog"
        className="inline-flex items-center gap-1.5 rounded-full border border-border-color bg-white/5 px-3 py-1.5 text-sm text-foreground-muted transition-all hover:border-border-hover hover:text-foreground"
      >
        <ArrowLeft size={14} />
        Quay lại blog
      </Link>

      <Reveal className="mt-6">
        <article>
          <header>
            <h1 className="font-display text-2xl font-semibold tracking-tight sm:text-4xl">
              {post.title}
            </h1>
            <div className="mt-2 flex items-center gap-3 font-mono text-sm text-foreground-muted">
              <time dateTime={post.date}>{formatDate(post.date)}</time>
              <span>·</span>
              <span>{post.readingTime}</span>
            </div>
          </header>

          <div className="mt-8">
            <PostBody content={post.content} />
          </div>
        </article>
      </Reveal>
    </div>
  );
}
