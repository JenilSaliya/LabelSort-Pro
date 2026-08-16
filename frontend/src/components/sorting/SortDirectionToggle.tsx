import { ArrowDownAZ, ArrowUpZA } from "lucide-react";
import { cn } from "@/lib/utils";

export interface SortDirectionToggleProps {
  reverse: boolean;
  onChange: (reverse: boolean) => void;
}

export function SortDirectionToggle({
  reverse,
  onChange,
}: SortDirectionToggleProps) {
  return (
    <div className="flex items-center gap-1.5 p-1 rounded-xl bg-secondary/80 border border-border/60">
      <button
        type="button"
        onClick={() => onChange(false)}
        className={cn(
          "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all",
          !reverse
            ? "bg-card text-foreground shadow-sm font-bold"
            : "text-muted-foreground hover:text-foreground hover:bg-muted/40"
        )}
      >
        <ArrowDownAZ className="h-4 w-4 text-primary" />
        <span>Ascending (A $\rightarrow$ Z)</span>
      </button>

      <button
        type="button"
        onClick={() => onChange(true)}
        className={cn(
          "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all",
          reverse
            ? "bg-card text-foreground shadow-sm font-bold"
            : "text-muted-foreground hover:text-foreground hover:bg-muted/40"
        )}
      >
        <ArrowUpZA className="h-4 w-4 text-primary" />
        <span>Descending (Z $\rightarrow$ A)</span>
      </button>
    </div>
  );
}
