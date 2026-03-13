import { useState } from "react";
import { UploadZone } from "./components/UploadZone";
import { ProgressBar } from "./components/ProgressBar";
import { HighlightsList } from "./components/HighlightsList";
import { ExportOptions } from "./components/ExportOptions";
import { uploadPdf, extractHighlights } from "./services/api";
import type { AppState, ExtractResponse } from "./types";

export default function App() {
  const [state, setState] = useState<AppState>({ stage: "idle" });

  const handleFile = async (file: File) => {
    try {
      // 1. Upload
      setState({ stage: "uploading", progress: 0 });
      const { upload_id, filename } = await uploadPdf(file, (pct) =>
        setState({ stage: "uploading", progress: pct })
      );

      // 2. Extract
      setState({ stage: "extracting", upload_id, filename });
      const result: ExtractResponse = await extractHighlights(upload_id);

      setState({ stage: "done", result });
    } catch (e) {
      setState({ stage: "error", message: (e as Error).message });
    }
  };

  const reset = () => setState({ stage: "idle" });

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="mx-auto max-w-2xl flex flex-col gap-8">

        {/* Header */}
        <header className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">PDF Highlight Extractor</h1>
          <p className="mt-2 text-gray-500">
            Drop a PDF to extract all highlighted text — download as TXT, Markdown, or JSON.
          </p>
        </header>

        {/* Upload stage */}
        {state.stage === "idle" && (
          <UploadZone onFile={handleFile} />
        )}

        {/* Upload progress */}
        {state.stage === "uploading" && (
          <div className="rounded-2xl bg-white border border-gray-200 p-8 shadow-sm">
            <ProgressBar label="Uploading…" value={state.progress} />
          </div>
        )}

        {/* Extraction in progress */}
        {state.stage === "extracting" && (
          <div className="rounded-2xl bg-white border border-gray-200 p-8 shadow-sm">
            <ProgressBar label={`Extracting highlights from "${state.filename}"…`} />
          </div>
        )}

        {/* Results */}
        {state.stage === "done" && (
          <div className="flex flex-col gap-6">
            <div className="rounded-2xl bg-white border border-gray-200 p-6 shadow-sm flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-gray-800">{state.result.filename}</p>
                <p className="text-sm text-gray-500">
                  {state.result.total} highlight{state.result.total !== 1 ? "s" : ""} found
                </p>
              </div>
              <button
                onClick={reset}
                className="text-sm text-gray-400 hover:text-gray-700 transition-colors"
              >
                ← New PDF
              </button>
            </div>

            <div className="rounded-2xl bg-white border border-gray-200 p-6 shadow-sm">
              <ExportOptions
                uploadId={state.result.upload_id}
                filename={state.result.filename}
              />
            </div>

            {state.result.total > 0 ? (
              <HighlightsList highlights={state.result.highlights} />
            ) : (
              <div className="rounded-2xl bg-white border border-gray-200 p-8 text-center shadow-sm">
                <p className="text-gray-500">No highlights found in this PDF.</p>
                <p className="text-sm text-gray-400 mt-1">
                  Make sure the PDF contains annotation-based highlights (not just colored text).
                </p>
              </div>
            )}
          </div>
        )}

        {/* Error state */}
        {state.stage === "error" && (
          <div className="rounded-2xl bg-red-50 border border-red-200 p-6 shadow-sm">
            <p className="font-semibold text-red-700">Something went wrong</p>
            <p className="mt-1 text-sm text-red-600">{state.message}</p>
            <button
              onClick={reset}
              className="mt-4 text-sm font-medium text-red-700 underline hover:no-underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center text-xs text-gray-400">
          PDFs are deleted automatically after 1 hour · No account required ·{" "}
          <a
            href="https://github.com/ddzeeuw1-ai/pdf-highlight-extractor"
            className="underline hover:text-gray-600"
            target="_blank"
            rel="noreferrer"
          >
            Open source on GitHub
          </a>
        </footer>
      </div>
    </div>
  );
}
