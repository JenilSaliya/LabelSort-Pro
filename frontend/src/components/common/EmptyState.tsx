import React from "react";
import { Button } from "../ui/Button";
import { FileQuestion } from "lucide-react";

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description: string;
  actionText?: string;
  onAction?: () => void;
}

export function EmptyState({
  icon = <FileQuestion className="h-10 w-10 text-muted-foreground" />,
  title,
  description,
  actionText,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 sm:p-12 text-center rounded-2xl border border-dashed border-border/80 bg-card/50">
      <div className="p-4 rounded-2xl bg-secondary/80 text-muted-foreground mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-bold text-foreground mb-1.5">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-sm mb-6 leading-relaxed">
        {description}
      </p>
      {actionText && onAction && (
        <Button onClick={onAction} variant="default">
          {actionText}
        </Button>
      )}
    </div>
  );
}
