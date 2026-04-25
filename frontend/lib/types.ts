export type Zone = {
  id: string;
  deviation: number;
  action: "REMOVE" | "FILL" | "KEEP";
  level: string;
  tool: string;
  grit: number[];
  risk: "LOW" | "MEDIUM" | "HIGH";
  warning?: string | null;
};

export type CompareResult = {
  zones: Zone[];
  steps: { step: number; action: string; tool: string; grit: number; zones: string[] }[];
  scan_quality: { quality: "LOW" | "MEDIUM" | "HIGH"; issues: string[]; suggestions: string[] };
  summary: Record<string, unknown>;
  heatmap: { zone: string; bbox: number[][]; deviation: number; action: string }[];
  report_json_path: string;
  report_pdf_path: string;
};
