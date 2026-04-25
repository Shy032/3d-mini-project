export type CapturedFrame = { id: string; blobUrl: string; accepted?: boolean; warnings?: string[] };

const framesKey = (scanId: string) => `trueform_frames_${scanId}`;

export function saveFrames(scanId: string, frames: CapturedFrame[]) {
  localStorage.setItem(framesKey(scanId), JSON.stringify(frames));
}

export function loadFrames(scanId: string): CapturedFrame[] {
  const raw = localStorage.getItem(framesKey(scanId));
  return raw ? (JSON.parse(raw) as CapturedFrame[]) : [];
}

export function saveJob(jobId: string, data: unknown) {
  localStorage.setItem(`trueform_job_${jobId}`, JSON.stringify(data));
}

export function loadJob(jobId: string): any {
  const raw = localStorage.getItem(`trueform_job_${jobId}`);
  return raw ? JSON.parse(raw) : null;
}
