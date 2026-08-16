import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?:
    | "default"
    | "secondary"
    | "outline"
    | "success"
    | "warning"
    | "destructive"
    | "glow";
  size?: "sm" | "default" | "lg";
}

export function Badge({
  className,
  variant = "default",
  size = "default",
  ...props
}: BadgeProps) {
  const variants = {
    default: "bg-primary/10 text-primary border-primary/20",
    secondary: "bg-secondary text-secondary-foreground border-border/60",
    outline: "border-border text-foreground/80 bg-transparent",
    success: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
    warning: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
    destructive: "bg-destructive/10 text-destructive border-destructive/20",
    glow: "bg-primary text-white shadow-sm border-transparent",
  };

  const sizes = {
    sm: "px-2 py-0.5 text-[11px] font-medium gap-1",
    default: "px-2.5 py-1 text-xs font-semibold gap-1.5",
    lg: "px-3.5 py-1.5 text-sm font-semibold gap-2",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border transition-colors select-none",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  );
}
