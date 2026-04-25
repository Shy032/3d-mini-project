import Link from "next/link";

export default function LandingPage() {
  return (
    <section className="space-y-6">
      <h1 className="text-4xl font-bold">Scan any object. Find the flaws. Get the exact fix plan.</h1>
      <p className="text-slate-300">
        TrueForm AI turns phone scans into visual flaw maps, deviation analysis, and step-by-step repair guidance for
        surfaces, shapes, and physical objects.
      </p>
      <div className="card space-y-3">
        <h2 className="text-xl font-semibold">Scan → Compare → Fix</h2>
        <p className="text-slate-300">Capture frames with your phone camera, compare to a target, then follow the Fix Plan.</p>
      </div>
      <Link href="/scan" className="inline-block rounded-lg bg-blue-600 px-5 py-3 text-lg font-semibold">Start Scan</Link>
    </section>
  );
}
