import { useState } from "react";
import type { ExportFormat } from "../types";
import { triggerDownload } from "../services/api";

interface Props {
  uploadId: string;
  filename: string;
}

const FORMATS: { value: ExportFormat; label: string; description: string }[] = [
  { value: "txt", label: "Plain Text", description: "Simple .txt, readable anywhere" },
  { value: "markdown", label: "Markdown", description: "For Obsidian, Logseq, Notion" },
  { value: "json", label: "JSON", description: "For developers & custom scripts" },
];

export function ExportOptions({ uploadId, filename }: Props) {
  const [loading, setLoading] = useState<ExportFormat | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async (format: ExportFormat) => {
    setLoading(format);
    setError(null);
    try {
      await triggerDownload(uploadId, format, filename);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm font-semibold text-gray-700">Export highlights as:</p>
      <div className="flex flex-wrap gap-2">
        {FORMATS.map(({ value, label, description }) => (
          <button
            key={value}
            onClick={() => handleDownload(value)}
            disabled={loading !== null}
            title={description}
            className={[
              "flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition-all",
              loading === value
                ? "border-blue-400 bg-blue-50 text-blue-600 cursor-wait"
                : "border-gray-300 bg-white text-gray-700 hover:border-blue-400 hover:text-blue-600 hover:bg-blue-50",
              loading !== null && loading !== value ? "opacity-50" : "",
            ].join(" ")}
          >
            {loading === value ? "↓ Downloading…" : `↓ ${label}`}
          </button>
        ))}
      </div>
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  );
}
