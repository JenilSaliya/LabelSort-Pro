import { Card } from "../ui/Card";
import { MarketplaceBadge } from "./MarketplaceBadge";
import { AnalysisResult } from "@/types";
import { FileText, Layers, Truck, BarChart2 } from "lucide-react";

export interface AnalysisSummaryProps {
  analysis: AnalysisResult;
}

export function AnalysisSummary({ analysis }: AnalysisSummaryProps) {
  const courierCount = analysis.courier_priority_options?.length || 0;
  const skuStats = analysis.field_statistics?.sku?.values || {};
  const uniqueSkuCount = Object.keys(skuStats).length;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 gap-4">
      {/* Marketplace & Total Labels */}
      <Card className="p-5 border-border/80 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Marketplace
          </span>
          <MarketplaceBadge marketplace={analysis.marketplace} />
        </div>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-extrabold text-foreground tracking-tight">
            {analysis.label_count}
          </p>
          <span className="text-xs font-medium text-muted-foreground">
            labels total
          </span>
        </div>
      </Card>

      {/* Pages */}
      <Card className="p-5 border-border/80 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Document Size
          </span>
          <div className="p-1.5 rounded-lg bg-primary/10 text-primary">
            <FileText className="h-4 w-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-extrabold text-foreground tracking-tight">
            {analysis.page_count}
          </p>
          <span className="text-xs font-medium text-muted-foreground">
            PDF pages
          </span>
        </div>
      </Card>

      {/* Couriers */}
      <Card className="p-5 border-border/80 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Couriers
          </span>
          <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
            <Truck className="h-4 w-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-extrabold text-foreground tracking-tight">
            {courierCount}
          </p>
          <span className="text-xs font-medium text-muted-foreground">
            partner networks
          </span>
        </div>
      </Card>

      {/* SKUs */}
      <Card className="p-5 border-border/80 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Unique SKUs
          </span>
          <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
            <BarChart2 className="h-4 w-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-extrabold text-foreground tracking-tight">
            {uniqueSkuCount || analysis.sortable_fields.find((f) => f.id === "sku")?.unique_values || 0}
          </p>
          <span className="text-xs font-medium text-muted-foreground">
            product variants
          </span>
        </div>
      </Card>
    </div>
  );
}
