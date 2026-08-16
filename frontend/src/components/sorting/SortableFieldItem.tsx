import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { GripVertical, CheckCircle2, Circle, ArrowDown, ArrowUp } from "lucide-react";
import { cn } from "@/lib/utils";

export interface SortableFieldItemProps {
  id: string;
  label: string;
  uniqueValues?: number;
  totalLabels?: number;
  rank: number;
  isSelected: boolean;
  onToggleSelect: () => void;
  onMoveUp?: () => void;
  onMoveDown?: () => void;
  canMoveUp?: boolean;
  canMoveDown?: boolean;
}

export function SortableFieldItem({
  id,
  label,
  uniqueValues,
  totalLabels,
  rank,
  isSelected,
  onToggleSelect,
  onMoveUp,
  onMoveDown,
  canMoveUp,
  canMoveDown,
}: SortableFieldItemProps) {
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

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "flex items-center justify-between p-3.5 sm:p-4 rounded-2xl border transition-all duration-150 select-none",
        isDragging
          ? "opacity-50 z-50 shadow-2xl scale-102 border-primary bg-primary/10"
          : isSelected
          ? "border-primary/50 bg-card hover:border-primary shadow-sm"
          : "border-border/70 bg-card/60 opacity-60 hover:opacity-100"
      )}
    >
      <div className="flex items-center gap-3 min-w-0">
        {/* Drag Handle */}
        <button
          type="button"
          {...attributes}
          {...listeners}
          className="cursor-grab active:cursor-grabbing p-1.5 rounded-lg text-muted-foreground/60 hover:text-foreground hover:bg-muted/80 transition-colors shrink-0"
          aria-label={`Reorder ${label}`}
        >
          <GripVertical className="h-5 w-5" />
        </button>

        {/* Priority Rank Indicator */}
        <div
          className={cn(
            "h-6 w-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0",
            isSelected
              ? "bg-primary text-white"
              : "bg-muted text-muted-foreground"
          )}
        >
          {rank}
        </div>

        {/* Label & Details */}
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-foreground truncate">
              {label}
            </span>
          </div>
          {uniqueValues !== undefined && (
            <p className="text-xs text-muted-foreground">
              {uniqueValues} unique {uniqueValues === 1 ? "value" : "values"}
            </p>
          )}
        </div>
      </div>

      {/* Right controls: accessible Move Up/Down + Toggle Inclusion */}
      <div className="flex items-center gap-1.5 shrink-0">
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

        <button
          type="button"
          onClick={onToggleSelect}
          className={cn(
            "p-1.5 rounded-xl transition-colors text-xs font-semibold flex items-center gap-1.5",
            isSelected
              ? "text-primary hover:bg-primary/10"
              : "text-muted-foreground hover:text-foreground hover:bg-muted"
          )}
        >
          {isSelected ? (
            <>
              <CheckCircle2 className="h-5 w-5 fill-primary text-white dark:text-card" />
              <span className="hidden sm:inline">Active</span>
            </>
          ) : (
            <>
              <Circle className="h-5 w-5 text-muted-foreground/40" />
              <span className="hidden sm:inline">Disabled</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
