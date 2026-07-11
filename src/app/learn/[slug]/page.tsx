import fs from "fs";
import path from "path";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import meta from "@content/_meta.json";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/Badge";
import Link from "next/link";

export async function generateStaticParams() {
  return meta.map((article) => ({
    slug: article.slug,
  }));
}

export default async function ArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const articleMeta = meta.find((m) => m.slug === slug);

  if (!articleMeta) notFound();

  const filePath = path.join(process.cwd(), "content", "learn", `${slug}.md`);
  
  const content = fs.readFileSync(filePath, "utf8");
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <nav className="flex items-center gap-2 text-sm text-zinc-500 dark:text-zinc-400 mb-8">
        <Link href="/learn/" className="hover:text-blue-600 dark:hover:text-blue-400">Guides</Link>
        <span>/</span>
        <span className="text-zinc-900 dark:text-zinc-100">{articleMeta.title}</span>
      </nav>

      <div className="mb-8">
        <Badge variant="info" className="mb-4">{articleMeta.category}</Badge>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100 sm:text-4xl">
          {articleMeta.title}
        </h1>
        <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400">
          {articleMeta.description}
        </p>
      </div>

      <div className="prose prose-zinc dark:prose-invert max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}
