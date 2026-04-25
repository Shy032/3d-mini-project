"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export default function ProcessingPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const qp = useSearchParams();
  const router = useRouter();
  const resultId = qp.get("resultId");
  const [status, setStatus] = useState<any>({ stage: "Uploading frames", progress: 0 });

  useEffect(() => {
    const timer = setInterval(async () => {
      const res = await fetch(`${API}/job/${jobId}/status`);
      const data = await res.json();
      setStatus(data);
      if (data.progress >= 100 && resultId) {
        clearInterval(timer);
        router.push(`/result/${resultId}`);
      }
    }, 900);
    return () => clearInterval(timer);
  }, [jobId, resultId, router]);

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">Processing</h1>
      <div className="card">
        <p>Stage: {status.stage}</p>
        <div className="mt-2 h-3 w-full rounded bg-slate-800">
          <div className="h-3 rounded bg-blue-500" style={{ width: `${status.progress || 0}%` }} />
        </div>
        <p className="mt-2 text-sm">{status.message}</p>
        <ul className="mt-3 list-disc pl-5 text-sm text-slate-300">
          <li>Uploading frames</li><li>Checking quality</li><li>Reconstructing scan</li><li>Aligning reference</li><li>Computing deviation</li><li>Generating action plan</li>
        </ul>
      </div>
    </section>
  );
}
