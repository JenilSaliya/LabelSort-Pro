import { useParams, Link, useNavigate } from "react-router-dom";
import { useAnalysis } from "@/features/labelsort/hooks/useAnalysis";
import { AnalysisSummary } from "@/components/analysis/AnalysisSummary";
import { CourierDistributionCard } from "@/components/analysis/CourierDistributionCard";
import { FieldStatisticsCard } from "@/components/analysis/FieldStatisticsCard";
import { PageHeader } from "@/components/common/PageHeader";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Button } from "@/components/ui/Button";
import { APP_ROUTES } from "@/lib/constants";
import { ArrowRight, SlidersHorizontal, Sparkles } from "lucide-react";

export function AnalysisPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();

  const {
    data: analysis,
    isLoading,
    error,
    refetch,
  } = useAnalysis(jobId);

  if (isLoading) {
    return (
      <LoadingState
        message="Analyzing shipping label data..."
        subMessage="Aggregating courier counts, SKU distributions, and size metrics"
      />
    );
  }

  if (error || !analysis || !jobId) {
    return (
      <ErrorState
        title="Analysis not found"
        message={error?.message || "Could not retrieve analysis for this job."}
        onRetry={() => refetch()}
      />
    );
  }

  const courierStats = analysis.field_statistics?.courier_partner?.values || {};
  const skuStats = analysis.field_statistics?.sku?.values || {};
  const sizeStats = analysis.field_statistics?.size?.values || {};

  return (
    <div className="space-y-6 max-w-6xl mx-auto animate-in fade-in duration-200">
      <PageHeader
        title="Label Batch Analytics"
        description="Comprehensive summary of products, courier logistics, and volume distribution extracted from your uploaded PDFs."
        actions={
          <Button
            variant="glow"
            size="default"
            onClick={() => navigate(APP_ROUTES.SORT(jobId))}
            rightIcon={<ArrowRight className="h-4 w-4" />}
          >
            Proceed to Sorting
          </Button>
        }
      />

      {/* Top Cards */}
      <AnalysisSummary analysis={analysis} />

      {/* Analytics Breakdown Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Courier Breakdown */}
        <CourierDistributionCard
          courierStats={courierStats}
          totalLabels={analysis.label_count}
        />

        {/* Size Breakdown */}
        {Object.keys(sizeStats).length > 0 && (
          <FieldStatisticsCard
            title="Size Distribution"
            fieldId="size"
            values={sizeStats}
            totalLabels={analysis.label_count}
          />
        )}

        {/* SKU Breakdown (Full Width if alone) */}
        <div className="md:col-span-2">
          <FieldStatisticsCard
            title="Product SKU"
            fieldId="sku"
            values={skuStats}
            totalLabels={analysis.label_count}
          />
        </div>
      </div>

      {/* Bottom Action Footer */}
      <div className="p-6 rounded-2xl bg-card border border-border/80 shadow-card flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1">
          <h4 className="text-base font-bold text-foreground">
            Configure Your Sorting Pipeline
          </h4>
          <p className="text-xs text-muted-foreground">
            Set custom courier rankings and organize picking bins by SKU.
          </p>
        </div>

        <Link to={APP_ROUTES.SORT(jobId)}>
          <Button
            variant="glow"
            size="lg"
            leftIcon={<SlidersHorizontal className="h-4 w-4" />}
            rightIcon={<ArrowRight className="h-4 w-4" />}
          >
            Configure Sorting Rules
          </Button>
        </Link>
      </div>
    </div>
  );
}
