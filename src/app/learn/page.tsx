import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import meta from "@content/_meta.json";

export default function LearnHub() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-4xl">
          Hardware Education Centre
        </h1>
        <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400">
          Learn the basics of PC hardware and make informed decisions for your build.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {meta.map((article) => (
          <Link key={article.slug} href={`/learn/${article.slug}`} className="group">
            <Card className="h-full p-6 transition-all group-hover:border-blue-500 group-hover:ring-1 group-hover:ring-blue-500">
              <div className="flex items-start justify-between mb-3">
                <Badge variant="secondary">{article.category}</Badge>
              </div>
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                {article.title}
              </h3>
              <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
                {article.description}
              </p>
              <div className="mt-6 flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400">
                Read Guide
                <svg width="14" height="14" viewBox="0, 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="transition-transform group-hover:translate-x-1">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
