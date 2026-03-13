import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

interface Props {
  onFile: (file: File) => void;
  disabled?: boolean;
}

export function UploadZone({ onFile, disabled }: Props) {
  const [dragOver, setDragOver] = useState(false);

  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted[0]) onFile(accepted[0]);
    },
    [onFile]
  );

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    disabled,
    onDragEnter: () => setDragOver(true),
    onDragLeave: () => setDragOver(false),
    onDropAccepted: () => setDragOver(false),
    onDropRejected: () => setDragOver(false),
  });

  return (
    <div
      {...getRootProps()}
      className={[
        "flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed p-16 transition-colors cursor-pointer select-none",
        disabled ? "opacity-40 cursor-not-allowed" : "hover:border-blue-500 hover:bg-blue-50",
        dragOver ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-gray-50",
      ].join(" ")}
    >
      <input {...getInputProps()} />
      <div className="text-5xl">📄</div>
      <p className="text-lg font-medium text-gray-700">
        Drop a PDF here, or <span className="text-blue-600 underline">browse</span>
      </p>
      <p className="text-sm text-gray-400">Only .pdf files · max 100 MB</p>
    </div>
  );
}
