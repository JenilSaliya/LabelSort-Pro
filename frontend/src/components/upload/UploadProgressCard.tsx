import React from "react";
import { UploadCloud, CheckCircle2, Clock, Zap, FileText } from "lucide-react";
import { Progress } from "../ui/Progress";

export interface UploadProgressCardProps {
  progress: number;
  fileCount: number;
  stageText?: string;
  pagesProcessed?: number | null;
  totalPages?: number | null;
  etaFormatted?: string | null;
  processingSpeedPps?: number | null;
  isComplete?: boolean;
}

export function UploadProgressCard({
  progress,
  fileCount,
  stageText = "Uploading and analyzing shipping labels...",
  pagesProcessed,
  totalPages,
  etaFormatted,
  processingSpeedPps,
  isComplete = false,
}: UploadProgressCardProps) {
  const hasPageTelemetry = Boolean(pagesProcessed && totalPages && totalPages > 0);
  const hasEta = Boolean(etaFormatted && etaFormatted !== "Ready");
  const hasSpeed = Boolean(processingSpeedPps && processingSpeedPps > 0);

  return (
    <div className="p-5 sm:p-6 rounded-2xl border border-primary/30 bg-card shadow-lg space-y-4 animate-in fade-in">
      {/* Header Info */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-primary text-white shrink-0 shadow-sm">
            {isComplete ? (
              <CheckCircle2 className="h-5 w-5" />
            ) : (
              <UploadCloud className="h-5 w-5 animate-pulse" />
            )}
          </div>
          <div>
            <p className="text-sm font-bold text-foreground">
              {isComplete ? "Upload Complete!" : "Processing Shipping Labels"}
            </p>
            <p className="text-xs text-muted-foreground">{stageText}</p>
          </div>
        </div>

        <span className="font-mono text-base font-extrabold text-primary bg-primary/10 dark:bg-primary/20 px-2.5 py-1 rounded-lg">
          {progress}%
        </span>
      </div>

      {/* Progress Bar */}
      <Progress value={progress} color="primary" className="h-2.5" />

      {/* Live Telemetry Badges (Page Counter, ETA, Processing Speed) */}
      {(hasPageTelemetry || hasEta || hasSpeed) && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1">
          {/* Page Counter */}
          {hasPageTelemetry && (
            <div className="flex items-center gap-2 p-2 rounded-xl bg-secondary/50 border border-border/60 text-xs">
              <FileText className="h-4 w-4 text-primary shrink-0" />
              <div className="truncate">
                <span className="text-[10px] uppercase font-bold text-muted-foreground block">Pages</span>
                <span className="font-semibold text-foreground">
                  {pagesProcessed} / {totalPages}
                </span>
              </div>
            </div>
          )}

          {/* Dynamic ETA */}
          {hasEta && (
            <div className="flex items-center gap-2 p-2 rounded-xl bg-secondary/50 border border-border/60 text-xs">
              <Clock className="h-4 w-4 text-amber-500 shrink-0" />
              <div className="truncate">
                <span className="text-[10px] uppercase font-bold text-muted-foreground block">Estimated Time</span>
                <span className="font-semibold text-foreground">
                  {etaFormatted}
                </span>
              </div>
            </div>
          )}

          {/* Processing Speed */}
          {hasSpeed && (
            <div className="flex items-center gap-2 p-2 rounded-xl bg-secondary/50 border border-border/60 text-xs col-span-2 sm:col-span-1">
              <Zap className="h-4 w-4 text-emerald-500 shrink-0" />
              <div className="truncate">
                <span className="text-[10px] uppercase font-bold text-muted-foreground block">Speed</span>
                <span className="font-semibold text-foreground">
                  ~{processingSpeedPps} pgs/s
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Bottom Status Info */}
      <div className="flex items-center justify-between text-xs text-muted-foreground pt-1 border-t border-border/40">
        <span className="flex items-center gap-1">
          <FileText className="h-3.5 w-3.5" />
          {fileCount} {fileCount === 1 ? "file" : "files"} in batch
        </span>
        <span>Please keep this window open</span>
      </div>
    </div>
  );
}
