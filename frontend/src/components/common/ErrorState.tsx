import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "../ui/Button";

export interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  actionText?: string;
}

export function ErrorState({
  title = "Something went wrong",
  message = "An error occurred while loading data. Please check your connection and try again.",
  onRetry,
  actionText = "Try Again",
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 sm:p-12 text-center rounded-2xl border border-destructive/20 bg-destructive/5 my-4">
      <div className="p-4 rounded-2xl bg-destructive/10 text-destructive mb-4">
        <AlertTriangle className="h-10 w-10" />
      </div>
      <h3 className="text-lg font-bold text-foreground mb-1.5">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-md mb-6 leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <Button
          onClick={onRetry}
          variant="outline"
          leftIcon={<RefreshCw className="h-4 w-4" />}
        >
          {actionText}
        </Button>
      )}
    </div>
  );
}
