interface Props {
  label: string;
  value?: number; // 0-100; omit for indeterminate
}

export function ProgressBar({ label, value }: Props) {
  const indeterminate = value === undefined;
  return (
    <div className="flex flex-col gap-2 w-full">
      <p className="text-sm text-gray-600">{label}</p>
      <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        {indeterminate ? (
          <div className="h-full w-1/3 bg-blue-500 rounded-full animate-[slide_1.2s_ease-in-out_infinite]" />
        ) : (
          <div
            className="h-full bg-blue-500 rounded-full transition-all duration-300"
            style={{ width: `${value}%` }}
          />
        )}
      </div>
      {!indeterminate && (
        <p className="text-xs text-gray-400 text-right">{value}%</p>
      )}
    </div>
  );
}
