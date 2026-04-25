"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export default function UploadPage() {
  const router = useRouter();
  const [scan, setScan] = useState<File | null>(null);
  const [reference, setReference] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!scan || !reference) return;
    setLoading(true);

    const up = async (file: File) => {
      const fd = new FormData();
      fd.append("file", file);
      const res = await fetch(`${API}/upload`, { method: "POST", body: fd });
      return (await res.json()) as { file: string };
    };

    const scanPath = await up(scan);
    const refPath = await up(reference);

    const compareBody = new FormData();
    compareBody.append("scan_file", scanPath.file);
    compareBody.append("reference_file", refPath.file);
    compareBody.append(
      "reference_spec_json",
      JSON.stringify({
        object_name: "example",
        units: "mm",
        tolerance_mm: 0.2,
        known_scale: { dimension: "width", value: 100 },
        zones: [{ id: "top_surface", type: "flat", target: "match_reference", max_allowed_excess_mm: 0.2 }],
      }),
    );

    const compareRes = await fetch(`${API}/compare`, { method: "POST", body: compareBody });
    const result = await compareRes.json();
    localStorage.setItem("trueform_result", JSON.stringify(result));
    router.push("/processing");
  };

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Upload scan + reference</h2>
      <div className="card space-y-3">
        <input type="file" accept=".ply,.obj,.stl,.glb,.usdz" onChange={(e) => setScan(e.target.files?.[0] ?? null)} />
        <input
          type="file"
          accept=".ply,.obj,.stl,.glb,.usdz"
          onChange={(e) => setReference(e.target.files?.[0] ?? null)}
        />
        <button className="rounded bg-blue-600 px-4 py-2 disabled:opacity-50" disabled={loading} onClick={handleSubmit}>
          {loading ? "Processing..." : "Upload + Compare"}
        </button>
      </div>
    </section>
  );
}
