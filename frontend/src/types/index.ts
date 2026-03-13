export interface Highlight {
  page: number;
  text: string;
}

export interface UploadResponse {
  upload_id: string;
  filename: string;
  size_bytes: number;
}

export interface ExtractResponse {
  upload_id: string;
  filename: string;
  total: number;
  highlights: Highlight[];
}

export type ExportFormat = "txt" | "markdown" | "json";

export type AppState =
  | { stage: "idle" }
  | { stage: "uploading"; progress: number }
  | { stage: "extracting"; upload_id: string; filename: string }
  | { stage: "done"; result: ExtractResponse }
  | { stage: "error"; message: string };
