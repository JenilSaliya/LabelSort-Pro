import React from "react";
import { FileText, Trash2 } from "lucide-react";
import { formatBytes } from "@/features/labelsort/utils/formatters";

export interface FileItemProps {
  file: File;
  onRemove: () => void;
  disabled?: boolean;
}

export function FileItem({ file, onRemove, disabled = false }: FileItemProps) {
  return (
    <div className="flex items-center justify-between p-3.5 sm:p-4 rounded-xl border border-border/80 bg-card hover:border-primary/40 transition-all group shadow-sm">
      <div className="flex items-center gap-3.5 min-w-0">
        <div className="p-2.5 rounded-lg bg-primary/10 text-primary shrink-0 group-hover:scale-105 transition-transform">
          <FileText className="h-5 w-5" />
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold text-foreground truncate max-w-[200px] sm:max-w-[320px] md:max-w-[400px]">
            {file.name}
          </p>
          <p className="text-xs text-muted-foreground font-mono">
            {formatBytes(file.size)}
          </p>
        </div>
      </div>

      <button
        type="button"
        onClick={onRemove}
        disabled={disabled}
        className="p-2 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors disabled:opacity-50"
        title="Remove file"
        aria-label={`Remove ${file.name}`}
      >
        <Trash2 className="h-4 w-4" />
      </button>
    </div>
  );
}
