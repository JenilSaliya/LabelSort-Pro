import { Link } from "react-router-dom";
import { PageHeader } from "@/components/common/PageHeader";
import { ComingSoonBadge } from "@/components/common/ComingSoonBadge";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { APP_ROUTES } from "@/lib/constants";
import { History, UploadCloud, Calendar, Clock, Database } from "lucide-react";

export function HistoryComingSoonPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-in fade-in duration-200">
      <PageHeader
        title="Sorting History"
        description="Persistent archive of past label batches, downloaded PDFs, and dispatched courier manifests."
        badge={<ComingSoonBadge text="Roadmap v1.2" />}
      />

      <Card className="p-8 sm:p-12 text-center border-dashed border-border/80 bg-card/50 space-y-6">
        <div className="p-4 rounded-2xl bg-primary/10 text-primary w-fit mx-auto">
          <History className="h-10 w-10" />
        </div>

        <div className="space-y-2 max-w-md mx-auto">
          <h3 className="text-xl font-bold text-foreground">
            Historical Session Storage Coming Soon
          </h3>
          <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
            In our next update with authenticated seller workspaces, you will be able to search past sorting jobs, re-download historical PDFs, and audit courier dispatch timestamps.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-lg mx-auto text-left pt-2">
          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <Calendar className="h-4 w-4 text-primary" />
              <span>30-Day Storage</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Keep searchable records of daily orders.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <Clock className="h-4 w-4 text-emerald-500" />
              <span>One-Click Re-Sort</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Re-run previous configs in seconds.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <Database className="h-4 w-4 text-indigo-500" />
              <span>Manifest Export</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Handover receipts for drivers.
            </p>
          </div>
        </div>

        <div className="pt-4">
          <Link to={APP_ROUTES.UPLOAD}>
            <Button variant="glow" leftIcon={<UploadCloud className="h-4 w-4" />}>
              Start a New Sorting Job
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
