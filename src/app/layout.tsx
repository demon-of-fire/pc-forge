import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import { Navigation } from "@/components/layout/Navigation";
import { Footer } from "@/components/layout/Footer";
import { SkipLink } from "@/components/accessibility/SkipLink";
import { OfflineIndicator } from "@/components/error/OfflineIndicator";
import { WebVitalsReporter } from "@/components/performance/WebVitals";
import { ServiceWorkerRegistration } from "@/components/performance/ServiceWorkerRegistration";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    template: "%s | PCForge",
    default: "PCForge — Open-Source PC Building Platform",
  },
  description:
    "Build, compare, and discover PC hardware. The open-source alternative to PCPartPicker.",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "PCForge",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#fafafa" },
    { media: "(prefers-color-scheme: dark)", color: "#09090b" },
  ],
  width: "device-width",
  initialScale: 1,
};

const themeScript = `
(function() {
  try {
    var theme = localStorage.getItem('pcforge-theme');
    var resolved = (theme === 'light') ? 'light' : (theme === 'dark') ? 'dark' : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.classList.add(resolved);
  } catch(e) {
    document.documentElement.classList.add('dark');
  }
})();
`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className={`${geistSans.variable} ${geistMono.variable}`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="min-h-screen flex flex-col bg-white text-zinc-900 antialiased dark:bg-zinc-950 dark:text-zinc-100">
        <Providers>
          <SkipLink />
          <Navigation />
          <main id="main-content" className="flex-1">
            {children}
          </main>
          <Footer />
          <OfflineIndicator />
          <WebVitalsReporter />
          <ServiceWorkerRegistration />
        </Providers>
      </body>
    </html>
  );
}
