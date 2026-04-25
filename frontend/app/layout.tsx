import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "SandingGuide AI",
  description: "Scan → Understand → Decide → Act",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-slate-800 bg-slate-900/80">
          <nav className="mx-auto flex max-w-6xl gap-5 p-4 text-sm">
            <Link href="/">Landing</Link>
            <Link href="/upload">Upload</Link>
            <Link href="/processing">Processing</Link>
            <Link href="/viewer">3D Viewer</Link>
            <Link href="/report">Report</Link>
          </nav>
        </header>
        <main className="mx-auto max-w-6xl p-5">{children}</main>
      </body>
    </html>
  );
}
