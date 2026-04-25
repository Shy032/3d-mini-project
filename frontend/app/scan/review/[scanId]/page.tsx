"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { loadFrames } from "@/lib/sessionStore";

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export default function ReviewPage() {
  const { scanId } = useParams<{ scanId: string }>();
  const router = useRouter();
  const [frames, setFrames] = useState(loadFrames(scanId));
  const [quality, setQuality] = useState<any>(null);

  useEffect(() => {
    const low = frames.length < 20;
    const med = frames.length >= 20 && frames.length < 40;
    setQuality({
      score: low ? "LOW" : med ? "MEDIUM" : "GOOD",
      issues: [
        ...(frames.length < 20 ? ["too few images"] : []),
        ...(frames.filter((f) => (f.warnings || []).includes("Image too blurry")).length > 5 ? ["blurry images"] : []),
        ...(frames.filter((f) => (f.warnings || []).includes("Too dark")).length > 5 ? ["low light"] : []),
        ...(frames.length < 40 ? ["not enough angle variation"] : []),
      ],
    });
  }, [frames]);

  const deleteFrame = (id: string) => setFrames((prev) => prev.filter((f) => f.id !== id));

  const processScan = async () => {
    const res = await fetch(`${API}/scan/${scanId}/process`, { method: "POST" });
    const data = await res.json();
    router.push(`/reference/${scanId}?jobId=${data.job_id}`);
  };

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">Scan Review</h1>
      <div className="card">
        <p>Scan ID: {scanId}</p>
        <p>Frame Count: {frames.length}</p>
        <p>Scan Quality: {quality?.score}</p>
        <p>Issues: {quality?.issues?.join(", ") || "none"}</p>
      </div>
      <div className="grid grid-cols-3 gap-2 sm:grid-cols-5">
        {frames.map((f) => (
          <button key={f.id} onClick={() => deleteFrame(f.id)} className="rounded border border-slate-700 p-1">
            <img src={f.blobUrl} alt="frame" className="h-20 w-full object-cover" />
            <span className="text-[10px]">Delete</span>
          </button>
        ))}
      </div>
      <button className="rounded bg-blue-600 px-4 py-3" onClick={processScan}>Process Scan</button>
    </section>
  );
}
