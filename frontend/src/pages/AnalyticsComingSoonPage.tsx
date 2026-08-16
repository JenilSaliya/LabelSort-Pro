import { Link } from "react-router-dom";
import { PageHeader } from "@/components/common/PageHeader";
import { ComingSoonBadge } from "@/components/common/ComingSoonBadge";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { APP_ROUTES } from "@/lib/constants";
import { BarChart3, UploadCloud, TrendingUp, PieChart, LineChart } from "lucide-react";

export function AnalyticsComingSoonPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-in fade-in duration-200">
      <PageHeader
        title="Aggregate Analytics"
        description="Cross-job intelligence showing monthly order volumes, top velocity SKUs, and courier pickup SLA breakdown."
        badge={<ComingSoonBadge text="Roadmap v1.3" />}
      />

      <Card className="p-8 sm:p-12 text-center border-dashed border-border/80 bg-card/50 space-y-6">
        <div className="p-4 rounded-2xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 w-fit mx-auto">
          <BarChart3 className="h-10 w-10" />
        </div>

        <div className="space-y-2 max-w-md mx-auto">
          <h3 className="text-xl font-bold text-foreground">
            Seller Analytics Dashboard In Progress
          </h3>
          <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
            Track which products are moving fastest, monitor courier allocation quotas, and optimize supplier replenishment schedules.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-lg mx-auto text-left pt-2">
          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <TrendingUp className="h-4 w-4 text-emerald-500" />
              <span>SKU Velocity</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Daily and weekly fastest movers.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <PieChart className="h-4 w-4 text-primary" />
              <span>Courier Share</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Ratio of Valmo, Delhivery, etc.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <LineChart className="h-4 w-4 text-amber-500" />
              <span>Order Trends</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Seasonal surge forecasting.
            </p>
          </div>
        </div>

        <div className="pt-4">
          <Link to={APP_ROUTES.UPLOAD}>
            <Button variant="glow" leftIcon={<UploadCloud className="h-4 w-4" />}>
              Process Current Labels
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
