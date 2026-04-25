"use client";

import { useMemo } from "react";
import { loadResult } from "@/lib/store";

export default function ReportPage() {
  const result = useMemo(() => (typeof window !== "undefined" ? loadResult() : null), []);

  if (!result) return <div className="card">No report generated yet.</div>;

  const jsonBlob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
  const jsonUrl = URL.createObjectURL(jsonBlob);

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Report</h2>
      <div className="card">
        <p>Scan quality: {result.scan_quality.quality}</p>
        <p>Issues: {result.scan_quality.issues.join(", ") || "none"}</p>
      </div>
      <div className="card">
        <h3 className="font-semibold">Action steps</h3>
        <ol className="ml-5 list-decimal">
          {result.steps.map((s) => (
            <li key={s.step}>{`${s.action} using ${s.tool} grit ${s.grit} on ${s.zones.join(", ")}`}</li>
          ))}
        </ol>
      </div>
      <div className="flex gap-3">
        <a className="rounded bg-green-600 px-3 py-2" href={jsonUrl} download="trueform_result.json">
          Download JSON
        </a>
        <a className="rounded bg-blue-600 px-3 py-2" href={result.report_pdf_path} target="_blank">
          Open PDF path (backend)
        </a>
      </div>
    </section>
  );
}
