"use client";

import { useMemo, useState } from "react";
import HeatmapViewer from "@/components/HeatmapViewer";
import { loadResult } from "@/lib/store";

export default function ViewerPage() {
  const result = useMemo(() => (typeof window !== "undefined" ? loadResult() : null), []);
  const [selected, setSelected] = useState<string | null>(null);

  if (!result) return <div className="card">No result yet. Upload data first.</div>;
  const active = result.zones.find((z) => z.id === selected) ?? result.zones[0];

  return (
    <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <div className="lg:col-span-2">
        <h2 className="mb-2 text-2xl font-semibold">3D Heatmap Viewer (split-ready MVP)</h2>
        <HeatmapViewer heatmap={result.heatmap} />
      </div>
      <aside className="card space-y-2">
        <h3 className="text-lg font-semibold">Zone Details</h3>
        <div className="grid gap-1">
          {result.zones.map((z) => (
            <button
              key={z.id}
              onClick={() => setSelected(z.id)}
              className="rounded border border-slate-700 px-2 py-1 text-left hover:bg-slate-800"
            >
              {z.id}: {z.action}
            </button>
          ))}
        </div>
        <hr className="border-slate-700" />
        <p>Zone: {active.id}</p>
        <p>Deviation: {active.deviation} mm</p>
        <p>Action: {active.action}</p>
        <p>Tool: {active.tool}</p>
        <p>Grit: {active.grit.join(" → ")}</p>
        <p>Risk: {active.risk}</p>
      </aside>
    </section>
  );
}
