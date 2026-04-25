import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "TrueForm AI",
  description: "Scan any object. Find the flaws. Get the exact fix plan.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="sticky top-0 z-10 border-b border-slate-800 bg-slate-950/95">
          <nav className="mx-auto flex max-w-6xl items-center gap-4 overflow-x-auto p-3 text-sm">
            <Link href="/" className="font-semibold">TrueForm AI</Link>
            <Link href="/scan">Scan</Link>
          </nav>
        </header>
        <main className="mx-auto max-w-6xl p-4">{children}</main>
      </body>
    </html>
  );
}
