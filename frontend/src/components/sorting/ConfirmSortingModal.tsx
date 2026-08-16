import { Modal } from "../ui/Modal";
import { Button } from "../ui/Button";
import { ArrowRight, Sparkles, CheckCircle2, Truck } from "lucide-react";
import { SortableField } from "@/types";

export interface ConfirmSortingModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isLoading: boolean;
  totalLabels: number;
  selectedFields: SortableField[];
  courierPriority: string[];
  reverse: boolean;
}

export function ConfirmSortingModal({
  isOpen,
  onClose,
  onConfirm,
  isLoading,
  totalLabels,
  selectedFields,
  courierPriority,
  reverse,
}: ConfirmSortingModalProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-primary" />
          <span>Ready to Sort {totalLabels} Labels?</span>
        </div>
      }
      description="Review your configured sorting hierarchy and courier priorities before processing."
      maxWidth="md"
      footer={
        <>
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={isLoading}
          >
            Modify Rules
          </Button>
          <Button
            variant="glow"
            onClick={onConfirm}
            isLoading={isLoading}
            rightIcon={<ArrowRight className="h-4 w-4" />}
          >
            Start Sorting Now
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        {/* Sort Fields Hierarchy */}
        <div className="p-4 rounded-xl bg-secondary/50 border border-border/70 space-y-2">
          <p className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
            Sort Order Priority
          </p>
          <div className="space-y-1.5">
            {selectedFields.map((field, idx) => (
              <div
                key={field.id}
                className="flex items-center gap-2.5 text-xs text-foreground font-medium"
              >
                <span className="h-5 w-5 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-[11px]">
                  {idx + 1}
                </span>
                <span>{field.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Courier Priority Ranking */}
        {courierPriority.length > 0 && (
          <div className="p-4 rounded-xl bg-secondary/50 border border-border/70 space-y-2">
            <div className="flex items-center gap-1.5">
              <Truck className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
              <p className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                Courier Handover Sequence
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-1">
              {courierPriority.map((courier, idx) => (
                <span
                  key={courier}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-card border border-border/80 shadow-xs"
                >
                  <span className="text-muted-foreground font-mono text-[10px]">
                    #{idx + 1}
                  </span>
                  <span>{courier}</span>
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Summary note */}
        <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
          <span>Sort Direction:</span>
          <span className="font-semibold text-foreground">
            {reverse ? "Descending (Z $\rightarrow$ A)" : "Ascending (A $\rightarrow$ Z)"}
          </span>
        </div>
      </div>
    </Modal>
  );
}
