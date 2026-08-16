import React, { useRef, useState } from "react";
import { UploadCloud, AlertCircle } from "lucide-react";
import { MAX_UPLOAD_SIZE_BYTES, MAX_UPLOAD_SIZE_MB } from "@/lib/constants";
import { cn } from "@/lib/utils";

export interface UploadDropzoneProps {
  onFilesSelected: (files: File[]) => void;
  disabled?: boolean;
  className?: string;
}

export function UploadDropzone({
  onFilesSelected,
  disabled = false,
  className,
}: UploadDropzoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndProcessFiles = (fileList: FileList | File[]) => {
    setErrorMessage(null);
    const validFiles: File[] = [];
    const invalidFiles: string[] = [];

    Array.from(fileList).forEach((file) => {
      const isPdf =
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf");

      if (!isPdf) {
        invalidFiles.push(`${file.name} (Not a PDF)`);
        return;
      }

      if (file.size > MAX_UPLOAD_SIZE_BYTES) {
        invalidFiles.push(
          `${file.name} (Exceeds ${MAX_UPLOAD_SIZE_MB}MB limit)`
        );
        return;
      }

      validFiles.push(file);
    });

    if (invalidFiles.length > 0) {
      setErrorMessage(invalidFiles.join(", "));
    }

    if (validFiles.length > 0) {
      onFilesSelected(validFiles);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (disabled) return;
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (disabled) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndProcessFiles(e.dataTransfer.files);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndProcessFiles(e.target.files);
      e.target.value = "";
    }
  };

  const handleClick = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className={cn("w-full space-y-2", className)}>
      <div
        onClick={handleClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative flex flex-col items-center justify-center p-6 sm:p-10 rounded-2xl border-2 border-dashed transition-all duration-200 cursor-pointer select-none text-center group",
          isDragOver
            ? "border-primary bg-primary/10 scale-[1.01] shadow-glow-primary"
            : "border-primary/40 dark:border-primary/30 hover:border-primary bg-primary/5 dark:bg-primary/[0.03] hover:bg-primary/[0.08]",
          disabled && "opacity-50 cursor-not-allowed pointer-events-none"
        )}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          onChange={handleInputChange}
          className="hidden"
          disabled={disabled}
        />

        {/* 3D-styled Upload Cloud Icon */}
        <div className="p-4 rounded-2xl bg-primary/15 text-primary mb-3.5 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary group-hover:text-white shadow-sm">
          <UploadCloud className="h-7 w-7" />
        </div>

        <h3 className="text-sm sm:text-base font-bold text-foreground mb-1">
          <span className="text-primary hover:underline">Click here</span> to upload or Drag & Drop Meesho Label PDFs
        </h3>

        <p className="text-xs text-muted-foreground max-w-xs leading-relaxed mb-3">
          Supported format: PDF • Up to {MAX_UPLOAD_SIZE_MB}MB
        </p>
      </div>

      {errorMessage && (
        <div className="flex items-center gap-2 p-2.5 rounded-xl bg-destructive/10 text-destructive text-xs font-medium border border-destructive/20 animate-in fade-in">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span className="truncate">{errorMessage}</span>
        </div>
      )}
    </div>
  );
}
