"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { saveFrames, CapturedFrame } from "@/lib/sessionStore";

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export default function ScanPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const router = useRouter();

  const [scanId, setScanId] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [isScanning, setIsScanning] = useState(false);
  const [frames, setFrames] = useState<CapturedFrame[]>([]);

  useEffect(() => {
    if (!window.isSecureContext && location.hostname !== "localhost") {
      setError("Camera requires HTTPS on mobile. Use localhost or an HTTPS tunnel.");
    }
    return () => {
      timerRef.current && clearInterval(timerRef.current);
      streamRef.current?.getTracks().forEach((t) => t.stop());
    };
  }, []);

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: "environment" },
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) videoRef.current.srcObject = stream;
      const res = await fetch(`${API}/scan/start`, { method: "POST" });
      const data = await res.json();
      setScanId(data.scan_id);
    } catch (e: any) {
      setError(e?.message?.includes("Permission") ? "Camera permission denied." : "No compatible camera found.");
    }
  };

  const captureOnce = async () => {
    if (!videoRef.current || !canvasRef.current || !scanId) return;
    const v = videoRef.current;
    const c = canvasRef.current;
    c.width = v.videoWidth || 1280;
    c.height = v.videoHeight || 720;
    const ctx = c.getContext("2d");
    if (!ctx) return;
    ctx.drawImage(v, 0, 0, c.width, c.height);

    const blob = await new Promise<Blob | null>((resolve) => c.toBlob(resolve, "image/jpeg", 0.85));
    if (!blob) return;

    const fd = new FormData();
    fd.append("file", new File([blob], `frame_${Date.now()}.jpg`, { type: "image/jpeg" }));
    const res = await fetch(`${API}/scan/${scanId}/frame`, { method: "POST", body: fd });
    const quality = await res.json();

    const newFrame: CapturedFrame = {
      id: quality.frame_id,
      blobUrl: URL.createObjectURL(blob),
      accepted: quality.accepted,
      warnings: quality.quality?.warnings ?? [],
    };
    const next = [newFrame, ...frames].slice(0, 40);
    setFrames(next);
    saveFrames(scanId, next);
  };

  const startAuto = () => {
    setIsScanning(true);
    timerRef.current = setInterval(captureOnce, 1500);
  };

  const pauseAuto = () => {
    setIsScanning(false);
    if (timerRef.current) clearInterval(timerRef.current);
  };

  const finish = async () => {
    pauseAuto();
    if (!scanId) return;
    await fetch(`${API}/scan/${scanId}/finish`, { method: "POST" });
    router.push(`/scan/review/${scanId}`);
  };

  return (
    <section className="space-y-3">
      <h1 className="text-2xl font-bold">Scan</h1>
      <p className="text-sm text-slate-300">Move slowly around the object. Keep it centered. Capture top/sides/bottom if possible.</p>
      {error && <div className="rounded bg-red-900/50 p-2 text-sm">{error}</div>}

      <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-black">
        <video ref={videoRef} autoPlay playsInline muted className="h-[60vh] w-full object-cover" />
        <canvas ref={canvasRef} className="hidden" />
        <div className="absolute right-3 top-3 rounded bg-black/60 px-3 py-1">Frames: {frames.length}</div>
      </div>

      <div className="grid grid-cols-2 gap-2 sm:grid-cols-5">
        <button className="rounded bg-slate-700 px-3 py-3" onClick={openCamera}>Open Camera</button>
        <button className="rounded bg-blue-600 px-3 py-3" onClick={startAuto}>Start</button>
        <button className="rounded bg-yellow-600 px-3 py-3" onClick={pauseAuto}>Pause</button>
        <button className="rounded bg-purple-600 px-3 py-3" onClick={captureOnce}>Capture</button>
        <button className="rounded bg-green-600 px-3 py-3" onClick={finish}>Finish Scan</button>
      </div>
      <div className="text-xs text-slate-400">Status: {isScanning ? "capturing" : "paused"} {scanId ? `| Scan ID: ${scanId}` : ""}</div>

      <div className="grid grid-cols-4 gap-2">
        {frames.map((f) => (
          <div key={f.id} className="rounded border border-slate-700 p-1">
            <img src={f.blobUrl} className="h-20 w-full object-cover" alt="frame" />
            <p className="text-[10px]">{f.accepted ? "accepted" : "review"}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
