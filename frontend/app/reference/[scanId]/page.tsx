"use client";

import { useParams, useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export default function ReferencePage() {
  const { scanId } = useParams<{ scanId: string }>();
  const qp = useSearchParams();
  const jobId = qp.get("jobId") || "";
  const router = useRouter();

  const [material, setMaterial] = useState("unknown");
  const [type, setType] = useState<"dimensions" | "json" | "mesh">("dimensions");
  const [mesh, setMesh] = useState<File | null>(null);
  const [jsonText, setJsonText] = useState('{"object_name":"sample","tolerance_mm":0.2}');
  const [dims, setDims] = useState({ object_type: "block", units: "mm", width: 120, height: 80, depth: 30, tolerance_mm: 0.2 });

  const submit = async () => {
    if (!jobId) return;
    const fd = new FormData();
    fd.append("material", material);

    if (type === "mesh" && mesh) fd.append("reference_mesh", mesh);
    if (type === "json") fd.append("reference_json", jsonText);
    if (type === "dimensions") fd.append("reference_dimensions", JSON.stringify(dims));

    await fetch(`${API}/job/${jobId}/reference`, { method: "POST", body: fd });
    const res = await fetch(`${API}/job/${jobId}/compare`, { method: "POST" });
    const data = await res.json();
    router.push(`/processing/${jobId}?resultId=${data.result_id}&scanId=${scanId}`);
  };

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">Compare Setup</h1>
      <div className="card space-y-3">
        <p>Scan ID: {scanId}</p>
        <p>Job ID: {jobId}</p>

        <label className="block">Material
          <select className="mt-1 w-full rounded bg-slate-800 p-2" value={material} onChange={(e) => setMaterial(e.target.value)}>
            <option>wood</option><option>plastic</option><option>metal</option><option>plaster/drywall</option><option>unknown</option>
          </select>
        </label>

        <div className="flex gap-2">
          <button className="rounded bg-slate-700 px-3 py-2" onClick={() => setType("mesh")}>Mesh</button>
          <button className="rounded bg-slate-700 px-3 py-2" onClick={() => setType("json")}>JSON</button>
          <button className="rounded bg-slate-700 px-3 py-2" onClick={() => setType("dimensions")}>Dimensions</button>
        </div>

        {type === "mesh" && <input type="file" accept=".obj,.ply,.stl,.glb" onChange={(e) => setMesh(e.target.files?.[0] || null)} />}
        {type === "json" && <textarea className="h-40 w-full rounded bg-slate-800 p-2" value={jsonText} onChange={(e) => setJsonText(e.target.value)} />}
        {type === "dimensions" && (
          <div className="grid grid-cols-2 gap-2">
            <input className="rounded bg-slate-800 p-2" value={dims.width} onChange={(e) => setDims({ ...dims, width: Number(e.target.value) })} />
            <input className="rounded bg-slate-800 p-2" value={dims.height} onChange={(e) => setDims({ ...dims, height: Number(e.target.value) })} />
            <input className="rounded bg-slate-800 p-2" value={dims.depth} onChange={(e) => setDims({ ...dims, depth: Number(e.target.value) })} />
            <input className="rounded bg-slate-800 p-2" value={dims.tolerance_mm} onChange={(e) => setDims({ ...dims, tolerance_mm: Number(e.target.value) })} />
          </div>
        )}

        <button className="rounded bg-blue-600 px-4 py-3" onClick={submit}>Run Compare</button>
      </div>
    </section>
  );
}
