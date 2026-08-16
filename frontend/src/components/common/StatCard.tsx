import React from "react";
import { Card } from "../ui/Card";
import { cn } from "@/lib/utils";

export interface StatCardProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  description?: string;
  change?: string;
  variant?: "default" | "primary" | "success" | "warning";
  className?: string;
}

export function StatCard({
  label,
  value,
  icon,
  description,
  variant = "default",
  className,
}: StatCardProps) {
  const iconVariants = {
    default: "bg-secondary text-foreground/80",
    primary: "bg-primary/10 text-primary",
    success: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
    warning: "bg-amber-500/10 text-amber-600 dark:text-amber-400",
  };

  return (
    <Card className={cn("p-5 border-border/70", className)}>
      <div className="flex items-center justify-between gap-4">
        <div className="space-y-1">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            {label}
          </p>
          <p className="text-2xl font-bold text-foreground tracking-tight">
            {value}
          </p>
          {description && (
            <p className="text-xs text-muted-foreground">{description}</p>
          )}
        </div>
        {icon && (
          <div
            className={cn(
              "p-3 rounded-xl shrink-0 flex items-center justify-center",
              iconVariants[variant]
            )}
          >
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
}
