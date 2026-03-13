import type { UploadResponse, ExtractResponse, ExportFormat } from "../types";

const BASE = import.meta.env.VITE_API_URL ?? "";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail ?? "An unexpected error occurred.");
  }
  return res.json() as Promise<T>;
}

export async function uploadPdf(
  file: File,
  onProgress?: (pct: number) => void
): Promise<UploadResponse> {
  return new Promise((resolve, reject) => {
    const form = new FormData();
    form.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${BASE}/api/upload`);

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText) as UploadResponse);
      } else {
        const body = JSON.parse(xhr.responseText ?? "{}");
        reject(new Error(body.detail ?? xhr.statusText));
      }
    };
    xhr.onerror = () => reject(new Error("Network error during upload."));
    xhr.send(form);
  });
}

export async function extractHighlights(
  uploadId: string
): Promise<ExtractResponse> {
  const res = await fetch(`${BASE}/api/extract/${uploadId}`, {
    method: "POST",
  });
  return handleResponse<ExtractResponse>(res);
}

export function exportUrl(uploadId: string, format: ExportFormat): string {
  return `${BASE}/api/export/${uploadId}?format=${format}`;
}

export async function triggerDownload(
  uploadId: string,
  format: ExportFormat,
  filename: string
): Promise<void> {
  const res = await fetch(exportUrl(uploadId, format), { method: "POST" });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "Export failed.");
  }
  const blob = await res.blob();
  const ext = format === "markdown" ? "md" : format;
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${filename} - Highlights.${ext}`;
  a.click();
  URL.revokeObjectURL(url);
}
