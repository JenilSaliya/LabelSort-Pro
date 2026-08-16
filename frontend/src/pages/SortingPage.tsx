import React, { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAnalysis } from "@/features/labelsort/hooks/useAnalysis";
import { useSortingConfig } from "@/features/labelsort/hooks/useSortingConfig";
import { useJob } from "@/features/labelsort/hooks/useJob";
import { useProcessJob } from "@/features/labelsort/hooks/useProcessJob";
import { SortableFieldList } from "@/components/sorting/SortableFieldList";
import { CourierPriorityList } from "@/components/sorting/CourierPriorityList";
import { SortDirectionToggle } from "@/components/sorting/SortDirectionToggle";
import { ConfirmSortingModal } from "@/components/sorting/ConfirmSortingModal";
import { MarketplaceBadge } from "@/components/analysis/MarketplaceBadge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { APP_ROUTES } from "@/lib/constants";
import { SortableField } from "@/types";
import { storageUtils } from "@/features/labelsort/utils/storageUtils";
import {
  ArrowRight,
  Truck,
  ListOrdered,
  RotateCcw,
  FileSpreadsheet,
  HelpCircle,
  ArrowLeft,
  CheckCircle2,
} from "lucide-react";
import { toast } from "sonner";

export function SortingPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();

  const {
    data: analysis,
    isLoading: analysisLoading,
    error: analysisError,
    refetch: refetchAnalysis,
  } = useAnalysis(jobId);

  const {
    data: sortingConfig,
    isLoading: configLoading,
  } = useSortingConfig(jobId);

  const { data: job } = useJob(jobId);
  const processMutation = useProcessJob(jobId || "");

  // Local sorting configuration state
  const [fields, setFields] = useState<SortableField[]>([]);
  const [selectedFieldIds, setSelectedFieldIds] = useState<string[]>([]);
  const [courierPriority, setCourierPriority] = useState<string[]>([]);
  const [reverse, setReverse] = useState(false);
  const [includeExcelReport, setIncludeExcelReport] = useState(true);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [hasRestoredPrefs, setHasRestoredPrefs] = useState(false);

  // Sync state from backend analysis and restore saved preferences
  useEffect(() => {
    if (analysis && !hasRestoredPrefs) {
      const saved = storageUtils.getSavedPreferences();

      // Setup fields
      let initialFields = [...analysis.sortable_fields];
      let initialSelectedIds = analysis.sortable_fields.map((f) => f.id);

      if (saved?.fieldIds && saved.fieldIds.length > 0) {
        const fieldMap = new Map(analysis.sortable_fields.map((f) => [f.id, f]));
        const ordered: SortableField[] = [];
        saved.fieldIds.forEach((id) => {
          const found = fieldMap.get(id);
          if (found) {
            ordered.push(found);
            fieldMap.delete(id);
          }
        });
        fieldMap.forEach((f) => ordered.push(f));
        initialFields = ordered;
        initialSelectedIds = saved.fieldIds.filter((id) =>
          analysis.sortable_fields.some((f) => f.id === id)
        );
      }

      // Setup courier priority
      let initialCouriers = [...(analysis.courier_priority_options || [])];
      if (saved?.courierPriority && saved.courierPriority.length > 0) {
        const availableCouriers = new Set(analysis.courier_priority_options || []);
        const orderedCouriers = saved.courierPriority.filter((c) =>
          availableCouriers.has(c)
        );
        (analysis.courier_priority_options || []).forEach((c) => {
          if (!orderedCouriers.includes(c)) {
            orderedCouriers.push(c);
          }
        });
        if (orderedCouriers.length > 0) {
          initialCouriers = orderedCouriers;
        }
      }

      setFields(initialFields);
      setSelectedFieldIds(
        initialSelectedIds.length > 0
          ? initialSelectedIds
          : analysis.sortable_fields.map((f) => f.id)
      );
      setCourierPriority(initialCouriers);
      if (saved?.reverse !== undefined) setReverse(saved.reverse);
      if (saved?.includeExcelReport !== undefined)
        setIncludeExcelReport(saved.includeExcelReport);

      setHasRestoredPrefs(true);
    }
  }, [analysis, hasRestoredPrefs]);

  // Save preferences automatically when changed
  const saveCurrentPreferences = (
    updatedFields: SortableField[],
    updatedSelected: string[],
    updatedCouriers: string[],
    updatedReverse: boolean,
    updatedExcel: boolean
  ) => {
    storageUtils.savePreferences({
      fieldIds: updatedFields
        .filter((f) => updatedSelected.includes(f.id))
        .map((f) => f.id),
      courierPriority: updatedCouriers,
      reverse: updatedReverse,
      includeExcelReport: updatedExcel,
    });
  };

  const handleOrderChange = (newFields: SortableField[]) => {
    setFields(newFields);
    saveCurrentPreferences(
      newFields,
      selectedFieldIds,
      courierPriority,
      reverse,
      includeExcelReport
    );
  };

  const handleToggleField = (fieldId: string) => {
    setSelectedFieldIds((prev) => {
      let updated: string[];
      if (prev.includes(fieldId)) {
        if (prev.length === 1) {
          toast.warning("At least one sorting field must remain active.");
          return prev;
        }
        updated = prev.filter((id) => id !== fieldId);
      } else {
        updated = [...prev, fieldId];
      }
      saveCurrentPreferences(
        fields,
        updated,
        courierPriority,
        reverse,
        includeExcelReport
      );
      return updated;
    });
  };

  const handleCourierOrderChange = (newCouriers: string[]) => {
    setCourierPriority(newCouriers);
    saveCurrentPreferences(
      fields,
      selectedFieldIds,
      newCouriers,
      reverse,
      includeExcelReport
    );
  };

  const handleReverseChange = (newReverse: boolean) => {
    setReverse(newReverse);
    saveCurrentPreferences(
      fields,
      selectedFieldIds,
      courierPriority,
      newReverse,
      includeExcelReport
    );
  };

  const handleToggleExcel = () => {
    const nextVal = !includeExcelReport;
    setIncludeExcelReport(nextVal);
    saveCurrentPreferences(
      fields,
      selectedFieldIds,
      courierPriority,
      reverse,
      nextVal
    );
    toast.info(
      nextVal ? "Excel statistics report enabled." : "Excel report disabled."
    );
  };

  const handleResetDefaults = () => {
    if (analysis) {
      storageUtils.clearPreferences();
      setFields(analysis.sortable_fields);
      setSelectedFieldIds(analysis.sortable_fields.map((f) => f.id));
      setCourierPriority(analysis.courier_priority_options || []);
      setReverse(false);
      setIncludeExcelReport(true);
      toast.info("Reset to default sorting rules.");
    }
  };

  const handleStartSorting = async () => {
    setIsConfirmOpen(false);
    try {
      const activeOrderedFieldIds = fields
        .filter((f) => selectedFieldIds.includes(f.id))
        .map((f) => f.id);

      const response = await processMutation.mutateAsync({
        fields: activeOrderedFieldIds,
        reverse,
        courier_priority: courierPriority,
      });

      if (response.success) {
        sessionStorage.setItem(
          "labelsort_include_excel",
          includeExcelReport ? "true" : "false"
        );
        toast.success("Labels sorted and PDF generated!");
        navigate(APP_ROUTES.RESULT(jobId || ""));
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to process labels.");
    }
  };

  if (analysisLoading || configLoading) {
    return (
      <LoadingState
        message="Loading sorting options..."
        subMessage="Preparing courier handover rules and SKU indexes"
      />
    );
  }

  if (analysisError || !analysis || !jobId) {
    return (
      <ErrorState
        title="Session expired or not found"
        message={
          analysisError?.message ||
          "Could not load analysis for this job. Please upload your files again."
        }
        onRetry={() => refetchAnalysis()}
        actionText="Reload Analysis"
      />
    );
  }

  const courierStats =
    analysis.field_statistics?.courier_partner?.values || {};
  const activeFieldsList = fields.filter((f) =>
    selectedFieldIds.includes(f.id)
  );
  const uniqueSkuCount =
    Object.keys(analysis.field_statistics?.sku?.values || {}).length ||
    analysis.sortable_fields.find((f) => f.id === "sku")?.unique_values ||
    0;

  return (
    <div className="space-y-4 max-w-full mx-auto animate-in fade-in duration-200">
      {/* Top Sticky Header with Metadata Badges + Quick Action Button */}
      <div className="sticky top-16 z-30 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-3.5 sm:p-4 rounded-2xl bg-card/95 backdrop-blur-md border border-border/80 shadow-sm transition-colors">
        {/* Left: Metadata Badges */}
        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
          <Link
            to={APP_ROUTES.UPLOAD}
            className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors mr-0.5"
            title="Back to upload"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>

          <MarketplaceBadge marketplace={analysis.marketplace} />

          <div className="px-2.5 py-1 rounded-full bg-secondary text-foreground font-bold text-xs border border-border/50">
            {analysis.label_count} labels
          </div>

          <div className="px-2.5 py-1 rounded-full bg-secondary text-foreground font-bold text-xs border border-border/50">
            {analysis.page_count} pages
          </div>

          {uniqueSkuCount > 0 && (
            <div className="hidden sm:inline-flex px-2.5 py-1 rounded-full bg-secondary text-foreground font-bold text-xs border border-border/50">
              {uniqueSkuCount} SKUs
            </div>
          )}

          {courierPriority.length > 0 && (
            <div className="hidden md:inline-flex px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold text-xs border border-emerald-500/20">
              {courierPriority.length} couriers
            </div>
          )}
        </div>

        {/* Right: Controls & Primary Action Button */}
        <div className="flex items-center gap-2 justify-between sm:justify-end shrink-0">
          {/* Excel Report On/Off Toggle */}
          <button
            type="button"
            onClick={handleToggleExcel}
            className={`flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl text-xs font-bold transition-all border shrink-0 ${
              includeExcelReport
                ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30"
                : "bg-secondary text-muted-foreground border-border hover:text-foreground"
            }`}
            title="Toggle Excel Statistics Generation"
          >
            <FileSpreadsheet className="h-3.5 w-3.5" />
            <span className="hidden xs:inline sm:inline">Excel:</span>
            <span>{includeExcelReport ? "ON" : "OFF"}</span>
            <span
              className={`h-2 w-2 rounded-full ${
                includeExcelReport
                  ? "bg-emerald-500 animate-pulse"
                  : "bg-muted-foreground/40"
              }`}
            />
          </button>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleResetDefaults}
            className="h-9 px-2 text-xs"
            title="Reset to default sorting rules"
          >
            <RotateCcw className="h-3.5 w-3.5" />
          </Button>

          {/* Compact, prominently positioned Generate Sorted PDF button */}
          <Button
            variant="glow"
            size="default"
            onClick={() => setIsConfirmOpen(true)}
            isLoading={processMutation.isPending}
            className="h-9 sm:h-10 px-3 sm:px-5 text-xs sm:text-sm font-bold shadow-md"
            rightIcon={<ArrowRight className="h-4 w-4" />}
          >
            Generate Sorted PDF
          </Button>
        </div>
      </div>

      {/* Main Sorting Workspace (Wide 2-Column Grid) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
        {/* Left Column: Sortable Fields Hierarchy */}
        <div className="lg:col-span-7 space-y-4">
          <Card className="p-4 sm:p-6 border-border/80 shadow-card">
            <CardHeader className="p-0 pb-3.5 flex flex-row items-center justify-between border-b border-border/60">
              <div className="space-y-0.5">
                <CardTitle className="text-sm sm:text-base flex items-center gap-2">
                  <ListOrdered className="h-4 w-4 text-primary" />
                  <span>Sort Type & Priority</span>
                </CardTitle>
                <p className="text-xs text-muted-foreground">
                  Drag items to reorder sorting sequence (Top = Highest Precedence)
                </p>
              </div>

              <Badge variant="secondary" size="sm">
                {activeFieldsList.length} Active
              </Badge>
            </CardHeader>

            <CardContent className="p-0 pt-3.5 space-y-4">
              <SortableFieldList
                fields={fields}
                selectedFieldIds={selectedFieldIds}
                onOrderChange={handleOrderChange}
                onToggleField={handleToggleField}
              />

              {/* Direction Toggle */}
              <div className="pt-3 border-t border-border/60 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5">
                <span className="text-xs font-bold text-foreground">
                  SKU & Field Sorting Direction
                </span>
                <SortDirectionToggle
                  reverse={reverse}
                  onChange={handleReverseChange}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Courier Partner Order */}
        <div className="lg:col-span-5 space-y-4">
          {courierPriority.length > 0 && (
            <Card className="p-4 sm:p-6 border-border/80 shadow-card">
              <CardHeader className="p-0 pb-3.5 flex flex-row items-center justify-between border-b border-border/60">
                <div className="space-y-0.5">
                  <CardTitle className="text-sm sm:text-base flex items-center gap-2">
                    <Truck className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                    <span>Courier Partner Order</span>
                  </CardTitle>
                  <p className="text-xs text-muted-foreground">
                    Drag to reorder pickup priority (Top = 1st Pickup)
                  </p>
                </div>

                <Badge variant="success" size="sm">
                  {courierPriority.length} Couriers
                </Badge>
              </CardHeader>

              <CardContent className="p-0 pt-3.5 space-y-3">
                <CourierPriorityList
                  couriers={courierPriority}
                  courierStats={courierStats}
                  onOrderChange={handleCourierOrderChange}
                />

                <div className="p-3 rounded-xl bg-secondary/50 border border-border/60 text-xs text-muted-foreground flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>
                    Your preferred courier rankings and sorting rules are automatically saved for your next upload batch.
                  </span>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Confirmation Modal */}
      <ConfirmSortingModal
        isOpen={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleStartSorting}
        isLoading={processMutation.isPending}
        totalLabels={analysis.label_count}
        selectedFields={activeFieldsList}
        courierPriority={courierPriority}
        reverse={reverse}
      />
    </div>
  );
}
