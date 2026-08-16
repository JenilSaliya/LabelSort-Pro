import { Loader2 } from "lucide-react";

export function LoadingState({
  message = "Loading...",
  subMessage,
}: {
  message?: string;
  subMessage?: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center min-h-[300px]">
      <div className="relative mb-4">
        <div className="h-12 w-12 rounded-full border-4 border-primary/20 border-t-primary animate-spin" />
        <Loader2 className="h-6 w-6 text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-spin-slow opacity-60" />
      </div>
      <p className="text-base font-semibold text-foreground">{message}</p>
      {subMessage && (
        <p className="text-xs text-muted-foreground mt-1 max-w-xs">{subMessage}</p>
      )}
    </div>
  );
}
