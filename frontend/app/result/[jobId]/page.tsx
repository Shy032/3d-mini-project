"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import HeatmapViewer from "@/components/HeatmapViewer";

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export default function ResultPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    fetch(`${API}/result/${jobId}`).then((r) => r.json()).then(setResult);
  }, [jobId]);

  if (!result) return <div className="card">Loading result...</div>;

  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">TrueForm AI Result</h1>
      {result.reconstruction?.warning && <div className="rounded bg-yellow-900/50 p-2">{result.reconstruction.warning}</div>}

      <div className="card"><h2 className="text-xl font-semibold">1. Flaw Map</h2><HeatmapViewer heatmap={result.heatmap || []} /></div>
      <div className="card"><h2 className="text-xl font-semibold">2. Deviation Summary</h2><pre className="text-xs">{JSON.stringify(result.summary, null, 2)}</pre></div>

      <div className="card"><h2 className="text-xl font-semibold">3. Fix Plan</h2>
        <ol className="list-decimal pl-5">{(result.repair_plan || []).map((s: any) => <li key={s.step}>{s.title} — {s.instruction}</li>)}</ol>
      </div>

      <div className="card"><h2 className="text-xl font-semibold">4. Tools & Materials</h2>
        <ul className="list-disc pl-5">{(result.zones || []).map((z: any) => <li key={z.id}>{z.id}: {z.tool} ({z.grit.join("→")})</li>)}</ul>
      </div>

      <div className="card"><h2 className="text-xl font-semibold">5. Risk Warnings</h2>
        <ul className="list-disc pl-5">{(result.zones || []).flatMap((z: any) => (z.instructions || []).filter((i: string) => i.toLowerCase().includes("risk") || i.toLowerCase().includes("low"))).map((w: string, i: number) => <li key={i}>{w}</li>)}</ul>
      </div>

      <div className="card"><h2 className="text-xl font-semibold">6. Rescan to Verify</h2>
        <p>After corrections, run another scan to verify and compare against target again.</p>
      </div>

      <div className="flex gap-2">
        <a className="rounded bg-green-600 px-4 py-2" href={`${API}/result/${jobId}/report.json`}>Download JSON report</a>
        <a className="rounded bg-blue-600 px-4 py-2" href={`${API}/result/${jobId}/report.pdf`}>Download PDF report</a>
      </div>
    </section>
  );
}
