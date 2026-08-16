import React from "react";
import { Check, Loader2, Circle, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export type StageStatus = "completed" | "active" | "pending" | "error";

export interface ProcessingStageItemProps {
  title: string;
  description?: string;
  status: StageStatus;
  isLast?: boolean;
}

export function ProcessingStageItem({
  title,
  description,
  status,
  isLast = false,
}: ProcessingStageItemProps) {
  const statusIcons = {
    completed: (
      <div className="h-7 w-7 rounded-full bg-emerald-500 text-white flex items-center justify-center shadow-sm shrink-0">
        <Check className="h-4 w-4 stroke-[3]" />
      </div>
    ),
    active: (
      <div className="h-7 w-7 rounded-full bg-primary text-white flex items-center justify-center shadow-glow-primary shrink-0">
        <Loader2 className="h-4 w-4 animate-spin" />
      </div>
    ),
    pending: (
      <div className="h-7 w-7 rounded-full bg-secondary border border-border text-muted-foreground flex items-center justify-center shrink-0">
        <Circle className="h-3 w-3 fill-muted-foreground/30 text-transparent" />
      </div>
    ),
    error: (
      <div className="h-7 w-7 rounded-full bg-destructive text-white flex items-center justify-center shrink-0">
        <AlertCircle className="h-4 w-4" />
      </div>
    ),
  };

  return (
    <div className="flex gap-4 group">
      {/* Icon and Connecting Line */}
      <div className="flex flex-col items-center">
        {statusIcons[status]}
        {!isLast && (
          <div
            className={cn(
              "w-0.5 flex-1 my-1.5 transition-colors duration-300",
              status === "completed"
                ? "bg-emerald-500/60"
                : status === "active"
                ? "bg-primary/40"
                : "bg-border/60"
            )}
            style={{ minHeight: "28px" }}
          />
        )}
      </div>

      {/* Text Details */}
      <div className="space-y-0.5 pb-5">
        <h4
          className={cn(
            "text-sm font-semibold tracking-tight transition-colors",
            status === "completed"
              ? "text-foreground font-bold"
              : status === "active"
              ? "text-primary font-bold"
              : status === "error"
              ? "text-destructive font-bold"
              : "text-muted-foreground/80 font-normal"
          )}
        >
          {title}
        </h4>
        {description && (
          <p className="text-xs text-muted-foreground leading-relaxed max-w-md">
            {description}
          </p>
        )}
      </div>
    </div>
  );
}
