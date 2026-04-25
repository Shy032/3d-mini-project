"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ProcessingPage() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => router.push("/viewer"), 1200);
    return () => clearTimeout(timer);
  }, [router]);

  return (
    <section className="card">
      <h2 className="text-xl font-semibold">Processing pipeline</h2>
      <ol className="ml-5 list-decimal text-slate-300">
        <li>Load + normalize</li>
        <li>ICP alignment</li>
        <li>Deviation + zone classification</li>
        <li>Action plan + risk analysis</li>
      </ol>
    </section>
  );
}
