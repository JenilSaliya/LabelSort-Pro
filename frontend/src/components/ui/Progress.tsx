import * as React from "react";
import { cn } from "@/lib/utils";

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number;
  max?: number;
  showLabel?: boolean;
  indeterminate?: boolean;
  color?: "primary" | "success" | "warning";
}

export function Progress({
  value = 0,
  max = 100,
  showLabel = false,
  indeterminate = false,
  color = "primary",
  className,
  ...props
}: ProgressProps) {
  const percentage = Math.min(Math.max(0, (value / max) * 100), 100);

  const colors = {
    primary: "bg-primary",
    success: "bg-emerald-500",
    warning: "bg-amber-500",
  };

  return (
    <div className="w-full space-y-1.5" {...props}>
      {showLabel && (
        <div className="flex justify-between text-xs font-medium text-muted-foreground">
          <span>Progress</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div
        className={cn(
          "relative h-2 w-full overflow-hidden rounded-full bg-secondary dark:bg-muted",
          className
        )}
      >
        {indeterminate ? (
          <div
            className={cn(
              "h-full w-1/3 rounded-full animate-[scan_1.5s_ease-in-out_infinite]",
              colors[color]
            )}
          />
        ) : (
          <div
            className={cn(
              "h-full transition-all duration-300 ease-out rounded-full",
              colors[color]
            )}
            style={{ width: `${percentage}%` }}
          />
        )}
      </div>
    </div>
  );
}
