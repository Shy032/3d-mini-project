"use client";

import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

const actionColor: Record<string, string> = {
  REMOVE: "#ef4444",
  KEEP: "#22c55e",
  FILL: "#3b82f6",
  NEAR: "#facc15",
};

export default function HeatmapViewer({ heatmap }: { heatmap: { zone: string; bbox: number[][]; action: string }[] }) {
  return (
    <div className="h-[420px] w-full">
      <Canvas camera={{ position: [3, 3, 4], fov: 50 }}>
        <ambientLight intensity={0.8} />
        <directionalLight position={[3, 5, 2]} intensity={0.8} />
        {heatmap.map((z) => {
          const [low, high] = z.bbox;
          const size: [number, number, number] = [high[0] - low[0], high[1] - low[1], high[2] - low[2]];
          const pos: [number, number, number] = [(high[0] + low[0]) / 2, (high[1] + low[1]) / 2, (high[2] + low[2]) / 2];
          return (
            <mesh key={z.zone} position={pos}>
              <boxGeometry args={size} />
              <meshStandardMaterial color={actionColor[z.action] ?? actionColor.NEAR} wireframe opacity={0.8} transparent />
            </mesh>
          );
        })}
        <OrbitControls />
      </Canvas>
    </div>
  );
}
