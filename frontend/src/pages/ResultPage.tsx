import React, { useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useJob } from "@/features/labelsort/hooks/useJob";
import { useAnalysis } from "@/features/labelsort/hooks/useAnalysis";
import { DownloadActions } from "@/components/results/DownloadActions";
import { PdfPreviewModal } from "@/components/results/PdfPreviewModal";
import { PdfViewer } from "@/components/results/PdfViewer";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { APP_ROUTES } from "@/lib/constants";
import { capitalizeMarketplace } from "@/features/labelsort/utils/formatters";
import {
  CheckCircle2,
  PlusCircle,
  Eye,
  SlidersHorizontal,
  ArrowLeft,
} from "lucide-react";

export function ResultPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [isPreviewModalOpen, setIsPreviewModalOpen] = useState(false);

  const { data: job, isLoading: jobLoading, error: jobError, refetch } = useJob(jobId);
  const { data: analysis } = useAnalysis(jobId);

  // Check if Excel report was enabled during sorting configuration
  const showExcel = sessionStorage.getItem("labelsort_include_excel") !== "false";

  if (jobLoading) {
    return (
      <LoadingState
        message="Loading sorted PDF results..."
        subMessage="Preparing download package and document preview"
      />
    );
  }

  if (jobError || !jobId) {
    return (
      <ErrorState
        title="Job not found"
        message={jobError?.message || "Could not locate this sorting session."}
        onRetry={() => refetch()}
      />
    );
  }

  const labelCount = analysis?.label_count || job?.label_groups || 0;
  const pageCount = analysis?.page_count || job?.page_count || 0;
  const marketplace = capitalizeMarketplace(job?.marketplace || analysis?.marketplace);

  return (
    <div className="space-y-5 max-w-5xl mx-auto animate-in fade-in duration-200">
      {/* Success Notification Banner */}
      <div className="p-4 sm:p-6 rounded-2xl bg-gradient-to-r from-emerald-500/10 via-teal-500/10 to-primary/10 border border-emerald-500/30 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 shadow-sm">
        <div className="flex items-center gap-3.5">
          <div className="h-11 w-11 rounded-xl bg-emerald-500 text-white flex items-center justify-center shadow-md shadow-emerald-500/20 shrink-0">
            <CheckCircle2 className="h-6 w-6 stroke-[2.5]" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h2 className="text-lg sm:text-xl font-extrabold text-foreground tracking-tight truncate">
                Processing Complete!
              </h2>
              <Badge variant="success" size="sm" className="hidden sm:inline-flex">
                Sorted & Ready
              </Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">
              Organized {labelCount} labels across {pageCount} pages.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 pt-2 sm:pt-0">
          <Link to={APP_ROUTES.SORT(jobId)} className="flex-1 sm:flex-none">
            <Button
              variant="outline"
              size="default"
              className="w-full sm:w-auto text-xs sm:text-sm"
              leftIcon={<SlidersHorizontal className="h-4 w-4 text-primary" />}
            >
              Change Rules & Re-sort
            </Button>
          </Link>

          <Link to={APP_ROUTES.UPLOAD} className="flex-1 sm:flex-none">
            <Button
              variant="ghost"
              size="default"
              className="w-full sm:w-auto text-xs sm:text-sm"
              leftIcon={<PlusCircle className="h-4 w-4" />}
            >
              New Job
            </Button>
          </Link>
        </div>
      </div>

      {/* Primary Download Actions */}
      <DownloadActions
        jobId={jobId}
        onOpenPreview={() => setIsPreviewModalOpen(true)}
        showExcel={showExcel}
      />

      {/* Embedded PDF Preview Map */}
      <Card className="border-border/80 shadow-card">
        <CardHeader className="pb-3 flex flex-row items-center justify-between border-b border-border/60">
          <div className="space-y-0.5">
            <CardTitle className="text-sm sm:text-base flex items-center gap-2">
              <Eye className="h-4 w-4 text-primary" />
              <span>Interactive PDF Preview</span>
            </CardTitle>
            <p className="text-xs text-muted-foreground">
              Review page ordering and barcode alignment directly in the browser
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Link to={APP_ROUTES.PREVIEW(jobId)}>
              <Button variant="ghost" size="sm" className="text-xs">
                Full Screen
              </Button>
            </Link>
          </div>
        </CardHeader>

        <CardContent className="p-3 sm:p-4">
          <PdfViewer jobId={jobId} className="w-full shadow-none border-0" />
        </CardContent>
      </Card>

      {/* Batch Metadata Summary */}
      <Card className="p-5 border-border/80 shadow-card">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
            Job Execution Summary
          </h4>
          <Link
            to={APP_ROUTES.SORT(jobId)}
            className="text-xs text-primary font-bold hover:underline flex items-center gap-1"
          >
            <SlidersHorizontal className="h-3 w-3" />
            <span>Re-configure sorting</span>
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="p-2.5 rounded-xl bg-secondary/50 space-y-0.5">
            <span className="text-muted-foreground text-[11px]">Marketplace</span>
            <p className="font-bold text-foreground truncate">{marketplace}</p>
          </div>
          <div className="p-2.5 rounded-xl bg-secondary/50 space-y-0.5">
            <span className="text-muted-foreground text-[11px]">Total Labels</span>
            <p className="font-bold text-foreground">{labelCount} labels</p>
          </div>
          <div className="p-2.5 rounded-xl bg-secondary/50 space-y-0.5">
            <span className="text-muted-foreground text-[11px]">Generated Pages</span>
            <p className="font-bold text-foreground">{pageCount} pages</p>
          </div>
          <div className="p-2.5 rounded-xl bg-secondary/50 space-y-0.5">
            <span className="text-muted-foreground text-[11px]">Output Format</span>
            <p className="font-bold text-foreground">
              {showExcel ? "PDF + Excel (.xlsx)" : "PDF Document"}
            </p>
          </div>
        </div>
      </Card>

      {/* Preview Modal */}
      <PdfPreviewModal
        isOpen={isPreviewModalOpen}
        onClose={() => setIsPreviewModalOpen(false)}
        jobId={jobId}
      />
    </div>
  );
}
