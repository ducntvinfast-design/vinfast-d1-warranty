import { MDXRemote } from "next-mdx-remote/rsc";

export function PostBody({ content }: { content: string }) {
  return (
    <div className="prose prose-headings:font-display max-w-none">
      <MDXRemote source={content} />
    </div>
  );
}
