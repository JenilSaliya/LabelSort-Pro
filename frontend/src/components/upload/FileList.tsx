import React from "react";
import { FileItem } from "./FileItem";
import { formatBytes } from "@/features/labelsort/utils/formatters";
import { Trash2, Plus } from "lucide-react";

export interface FileListProps {
  files: File[];
  onRemove: (index: number) => void;
  onClearAll: () => void;
  onAddMore: () => void;
  disabled?: boolean;
}

export function FileList({
  files,
  onRemove,
  onClearAll,
  onAddMore,
  disabled = false,
}: FileListProps) {
  if (files.length === 0) return null;

  const totalBytes = files.reduce((acc, f) => acc + f.size, 0);

  return (
    <div className="space-y-3 w-full animate-in fade-in">
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          <span>SELECTED FILES ({files.length})</span>
          <span>•</span>
          <span className="font-mono text-foreground font-bold">{formatBytes(totalBytes)}</span>
        </div>

        <button
          type="button"
          onClick={onClearAll}
          disabled={disabled}
          className="text-xs text-muted-foreground hover:text-destructive flex items-center gap-1 transition-colors"
        >
          <Trash2 className="h-3.5 w-3.5" />
          <span>Clear all</span>
        </button>
      </div>

      <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
        {files.map((file, index) => (
          <FileItem
            key={`${file.name}-${file.size}-${index}`}
            file={file}
            onRemove={() => onRemove(index)}
            disabled={disabled}
          />
        ))}
      </div>

      <button
        type="button"
        onClick={onAddMore}
        disabled={disabled}
        className="w-full py-3 rounded-2xl border-2 border-dashed border-primary/50 hover:border-primary text-xs font-bold text-primary hover:bg-primary/5 active:scale-[0.99] transition-all flex items-center justify-center gap-2 cursor-pointer"
      >
        <Plus className="h-4 w-4" />
        <span>Add More PDF Files</span>
      </button>
    </div>
  );
}
