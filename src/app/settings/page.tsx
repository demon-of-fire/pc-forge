"use client";

import { useTheme } from "@/lib/themes";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export default function SettingsPage() {
  const { theme, setTheme, resolved } = useTheme();

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100">Settings</h1>
        <p className="mt-4 text-zinc-600 dark:text-zinc-400">
          Customize your PCForge experience.
        </p>
      </div>

      <div className="space-y-8">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Appearance</h3>
              <p className="text-sm text-zinc-500 dark:text-zinc-400">
                Adjust the website theme to your preference.
              </p>
            </div>
            <Badge variant="secondary">
              Current: {resolved.toUpperCase()}
            </Badge>
          </div>
          
          <div className="mt-6 flex gap-3">
            {(["light", "dark", "system"] as const).map((t) => (
              <Button
                key={t}
                variant={theme === t ? "primary" : "outline"}
                className="capitalize flex-1"
                onClick={() => setTheme(t)}
              >
                {t}
              </Button>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Accessibility</h3>
              <p className="text-sm text-zinc-500 dark:text-zinc-400">
                Optimize the site for screen readers and keyboard navigation.
              </p>
            </div>
          </div>
          <div className="mt-6 space-y-4">
            <div className="flex items-center justify-between p-3 rounded-lg border border-zinc-200 dark:border-zinc-800">
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">High Contrast Mode</span>
              <div className="h-6 w-11 rounded-full bg-zinc-200 dark:bg-zinc-700 relative cursor-pointer">
                <div className="absolute left-1 top-1 h-4 w-4 rounded-full bg-white shadow-sm transition-all" />
              </div>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg border border-zinc-200 dark:border-zinc-800">
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Reduce Motion</span>
              <div className="h-6 w-11 rounded-full bg-blue-600 relative cursor-pointer">
                <div className="absolute right-1 top-1 h-4 w-4 rounded-full bg-white shadow-sm transition-all" />
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
