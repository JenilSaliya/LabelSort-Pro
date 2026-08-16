import { Link } from "react-router-dom";
import { PageHeader } from "@/components/common/PageHeader";
import { ComingSoonBadge } from "@/components/common/ComingSoonBadge";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { APP_ROUTES } from "@/lib/constants";
import { Settings, UploadCloud, Sliders, Users, Key } from "lucide-react";

export function SettingsComingSoonPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-in fade-in duration-200">
      <PageHeader
        title="Workspace Settings & Rules"
        description="Configure default sorting templates, courier priority preferences, team accounts, and API access keys."
        badge={<ComingSoonBadge text="Roadmap v1.4" />}
      />

      <Card className="p-8 sm:p-12 text-center border-dashed border-border/80 bg-card/50 space-y-6">
        <div className="p-4 rounded-2xl bg-secondary text-foreground w-fit mx-auto">
          <Settings className="h-10 w-10" />
        </div>

        <div className="space-y-2 max-w-md mx-auto">
          <h3 className="text-xl font-bold text-foreground">
            Custom Automation Rules & Team Settings
          </h3>
          <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
            Save persistent presets for different warehouse shifts, configure multi-user access permissions, and generate webhook API keys.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-lg mx-auto text-left pt-2">
          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <Sliders className="h-4 w-4 text-primary" />
              <span>Preset Rules</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Save 1-click sorting templates.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <Users className="h-4 w-4 text-emerald-500" />
              <span>Team Accounts</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Role-based warehouse logins.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-secondary/50 border border-border/60 space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-foreground">
              <Key className="h-4 w-4 text-amber-500" />
              <span>API Keys</span>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Direct ERP / WMS integrations.
            </p>
          </div>
        </div>

        <div className="pt-4">
          <Link to={APP_ROUTES.UPLOAD}>
            <Button variant="glow" leftIcon={<UploadCloud className="h-4 w-4" />}>
              Back to Upload
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
