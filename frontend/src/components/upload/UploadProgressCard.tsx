import React from "react";
import { UploadCloud, CheckCircle2, FileText } from "lucide-react";
import { Progress } from "../ui/Progress";

export interface UploadProgressCardProps {
  progress: number;
  fileCount: number;
  stageText?: string;
  isComplete?: boolean;
}

export function UploadProgressCard({
  progress,
  fileCount,
  stageText = "Uploading and analyzing shipping labels...",
  isComplete = false,
}: UploadProgressCardProps) {
  return (
    <div className="p-5 rounded-2xl border border-primary/20 bg-primary/5 dark:bg-primary/10 shadow-sm space-y-3 animate-in fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-primary text-white shrink-0 shadow-sm">
            {isComplete ? (
              <CheckCircle2 className="h-5 w-5" />
            ) : (
              <UploadCloud className="h-5 w-5 animate-bounce" />
            )}
          </div>
          <div>
            <p className="text-sm font-bold text-foreground">
              {isComplete ? "Upload Complete!" : "Uploading & Processing..."}
            </p>
            <p className="text-xs text-muted-foreground">{stageText}</p>
          </div>
        </div>

        <span className="font-mono text-sm font-bold text-primary">
          {progress}%
        </span>
      </div>

      <Progress value={progress} color="primary" />

      <div className="flex items-center justify-between text-xs text-muted-foreground pt-1">
        <span className="flex items-center gap-1">
          <FileText className="h-3.5 w-3.5" />
          {fileCount} {fileCount === 1 ? "file" : "files"} in batch
        </span>
        <span>Please keep this window open</span>
      </div>
    </div>
  );
}
