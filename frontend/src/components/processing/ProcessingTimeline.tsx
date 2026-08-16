import React from "react";
import { ProcessingStageItem, StageStatus } from "./ProcessingStageItem";
import { JobWorkflowStage, JobMetadata, AnalysisResult } from "@/types";
import { capitalizeMarketplace } from "@/features/labelsort/utils/formatters";

export interface ProcessingTimelineProps {
  currentStage: JobWorkflowStage;
  job?: JobMetadata | null;
  analysis?: AnalysisResult | null;
}

export function ProcessingTimeline({
  currentStage,
  job,
  analysis,
}: ProcessingTimelineProps) {
  // Compute the status of each stage
  const getStatus = (targetStage: JobWorkflowStage): StageStatus => {
    const stageOrder: JobWorkflowStage[] = [
      "upload_completed",
      "marketplace_detected",
      "labels_extracted",
      "analysis_ready",
      "statistics_generated",
      "waiting_for_sort",
      "processing",
      "completed",
    ];

    if (currentStage === "error") {
      return "error";
    }

    const currentIndex = stageOrder.indexOf(currentStage);
    const targetIndex = stageOrder.indexOf(targetStage);

    if (currentIndex > targetIndex) return "completed";
    if (currentIndex === targetIndex) return "active";
    return "pending";
  };

  const marketplaceName = capitalizeMarketplace(job?.marketplace || analysis?.marketplace || "Meesho");
  const labelCount = analysis?.label_count || job?.label_groups || 0;
  const pageCount = analysis?.page_count || job?.page_count || 0;
  const sortFieldsCount = analysis?.sortable_fields?.length || 0;

  const stages = [
    {
      id: "upload_completed" as JobWorkflowStage,
      title: "PDF Upload Complete",
      description: "Files safely uploaded and verified by server.",
    },
    {
      id: "marketplace_detected" as JobWorkflowStage,
      title: "Marketplace Detected",
      description: `${marketplaceName} shipping label format identified.`,
    },
    {
      id: "labels_extracted" as JobWorkflowStage,
      title: "Labels Extracted",
      description: labelCount > 0 ? `Found ${labelCount} shipping labels across ${pageCount} pages.` : "Extracting label blocks and barcode metadata.",
    },
    {
      id: "analysis_ready" as JobWorkflowStage,
      title: "Analysis Ready",
      description: sortFieldsCount > 0 ? `${sortFieldsCount} sortable criteria and courier rules discovered.` : "Building inventory counts and SKU distribution.",
    },
    {
      id: "statistics_generated" as JobWorkflowStage,
      title: "Statistics Generated",
      description: "Excel breakdown generated and ready for export.",
    },
    {
      id: "waiting_for_sort" as JobWorkflowStage,
      title: "Sorting Strategy Setup",
      description: "Configure courier priorities and sort hierarchy.",
    },
    {
      id: "processing" as JobWorkflowStage,
      title: "Processing & Rebuilding PDF",
      description: "Reordering pages and assembling sorted PDF document.",
    },
    {
      id: "completed" as JobWorkflowStage,
      title: "Sorted Output Ready",
      description: "Sorted PDF and Excel reports ready for download.",
    },
  ];

  return (
    <div className="p-6 rounded-2xl bg-card border border-border/80 shadow-card space-y-2">
      <h3 className="text-base font-bold text-foreground mb-4 flex items-center justify-between">
        <span>Processing Lifecycle</span>
        <span className="text-xs font-normal text-muted-foreground">
          Step-by-step verified execution
        </span>
      </h3>

      <div className="pt-2">
        {stages.map((stage, index) => (
          <ProcessingStageItem
            key={stage.id}
            title={stage.title}
            description={stage.description}
            status={getStatus(stage.id)}
            isLast={index === stages.length - 1}
          />
        ))}
      </div>
    </div>
  );
}
