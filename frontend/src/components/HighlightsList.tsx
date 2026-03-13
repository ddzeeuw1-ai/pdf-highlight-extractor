import { useState } from "react";
import type { Highlight } from "../types";

interface Props {
  highlights: Highlight[];
}

export function HighlightsList({ highlights }: Props) {
  const [search, setSearch] = useState("");
  const [copied, setCopied] = useState<number | null>(null);

  const filtered = search.trim()
    ? highlights.filter(
        (h) =>
          h.text.toLowerCase().includes(search.toLowerCase()) ||
          String(h.page).includes(search)
      )
    : highlights;

  const copyToClipboard = async (text: string, index: number) => {
    await navigator.clipboard.writeText(text);
    setCopied(index);
    setTimeout(() => setCopied(null), 1500);
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between gap-4">
        <p className="text-sm text-gray-500">
          Showing <strong>{filtered.length}</strong> of{" "}
          <strong>{highlights.length}</strong> highlights
        </p>
        <input
          type="search"
          placeholder="Search highlights…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm w-56 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <ul className="flex flex-col gap-3">
        {filtered.map((h, i) => (
          <li
            key={i}
            className="group relative rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between gap-2">
              <span className="shrink-0 rounded-md bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-600">
                Page {h.page}
              </span>
              <button
                onClick={() => copyToClipboard(h.text, i)}
                className="shrink-0 text-xs text-gray-400 hover:text-blue-600 transition-colors opacity-0 group-hover:opacity-100"
                aria-label="Copy highlight text"
              >
                {copied === i ? "✓ Copied" : "Copy"}
              </button>
            </div>
            <p className="mt-2 text-sm leading-relaxed text-gray-700">{h.text}</p>
          </li>
        ))}
      </ul>

      {filtered.length === 0 && (
        <p className="text-center text-sm text-gray-400 py-8">
          No highlights match your search.
        </p>
      )}
    </div>
  );
}
