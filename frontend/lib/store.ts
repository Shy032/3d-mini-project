import { CompareResult } from "./types";

const KEY = "trueform_result";

export function saveResult(result: CompareResult) {
  localStorage.setItem(KEY, JSON.stringify(result));
}

export function loadResult(): CompareResult | null {
  const raw = localStorage.getItem(KEY);
  return raw ? (JSON.parse(raw) as CompareResult) : null;
}
