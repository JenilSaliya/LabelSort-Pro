import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { GripVertical, Truck, ArrowUp, ArrowDown } from "lucide-react";
import { cn } from "@/lib/utils";

export interface CourierPriorityItemProps {
  id: string;
  courierName: string;
  labelCount?: number;
  priorityRank: number;
  totalCouriers: number;
  onMoveUp?: () => void;
  onMoveDown?: () => void;
  canMoveUp?: boolean;
  canMoveDown?: boolean;
}

export function CourierPriorityItem({
  id,
  courierName,
  labelCount,
  priorityRank,
  totalCouriers,
  onMoveUp,
  onMoveDown,
  canMoveUp,
  canMoveDown,
}: CourierPriorityItemProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const isHighestPriority = priorityRank === 1;

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "flex items-center justify-between p-3.5 sm:p-4 rounded-2xl border transition-all duration-150 select-none bg-card",
        isDragging
          ? "opacity-50 z-50 shadow-2xl scale-102 border-emerald-500 bg-emerald-500/10"
          : isHighestPriority
          ? "border-emerald-500/50 hover:border-emerald-500 shadow-sm"
          : "border-border/80 hover:border-border"
      )}
    >
      <div className="flex items-center gap-3.5 min-w-0">
        {/* Drag Handle */}
        <button
          type="button"
          {...attributes}
          {...listeners}
          className="cursor-grab active:cursor-grabbing p-1.5 rounded-lg text-muted-foreground/60 hover:text-foreground hover:bg-muted/80 transition-colors shrink-0"
          aria-label={`Reorder priority for ${courierName}`}
        >
          <GripVertical className="h-5 w-5" />
        </button>

        {/* Priority Rank */}
        <div
          className={cn(
            "h-7 w-7 rounded-xl flex items-center justify-center text-xs font-extrabold shrink-0",
            isHighestPriority
              ? "bg-emerald-500 text-white shadow-sm"
              : "bg-secondary text-foreground/80 border border-border/60"
          )}
        >
          {priorityRank}
        </div>

        {/* Courier Details */}
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <Truck className="h-4 w-4 text-muted-foreground shrink-0" />
            <span className="text-sm font-bold text-foreground truncate">
              {courierName}
            </span>
          </div>
          {isHighestPriority && (
            <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
              Highest Priority (First in batch)
            </span>
          )}
        </div>
      </div>

      <div className="flex items-center gap-3 shrink-0">
        {labelCount !== undefined && (
          <span className="font-mono text-xs text-muted-foreground bg-secondary/80 px-2.5 py-1 rounded-lg">
            {labelCount} {labelCount === 1 ? "label" : "labels"}
          </span>
        )}

        {/* Accessible mobile reorder buttons */}
        <div className="flex items-center sm:hidden">
          {onMoveUp && canMoveUp && (
            <button
              type="button"
              onClick={onMoveUp}
              className="p-1 text-muted-foreground hover:text-foreground"
              title="Move Up"
            >
              <ArrowUp className="h-4 w-4" />
            </button>
          )}
          {onMoveDown && canMoveDown && (
            <button
              type="button"
              onClick={onMoveDown}
              className="p-1 text-muted-foreground hover:text-foreground"
              title="Move Down"
            >
              <ArrowDown className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
