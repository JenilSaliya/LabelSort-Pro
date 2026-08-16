import { Link, useLocation } from "react-router-dom";
import {
  UploadCloud,
  FileSpreadsheet,
  History,
  BarChart3,
  Settings,
  Code2,
  CheckCircle2,
  X,
  Layers,
  ArrowRight,
} from "lucide-react";
import { APP_ROUTES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { ComingSoonBadge } from "../common/ComingSoonBadge";
import { Button } from "../ui/Button";

export interface SidebarProps {
  activeJobId?: string | null;
  isOpenMobile?: boolean;
  onCloseMobile?: () => void;
  serverOnline?: boolean;
}

export function Sidebar({
  activeJobId,
  isOpenMobile = false,
  onCloseMobile,
  serverOnline = true,
}: SidebarProps) {
  const location = useLocation();

  const mainLinks = [
    {
      label: "New Sorting Job",
      to: APP_ROUTES.UPLOAD,
      icon: UploadCloud,
      active: location.pathname === APP_ROUTES.UPLOAD || location.pathname === APP_ROUTES.WORKSPACE,
    },
    ...(activeJobId
      ? [
          {
            label: "Current Job",
            to: APP_ROUTES.SORT(activeJobId),
            icon: FileSpreadsheet,
            active: location.pathname.startsWith(`/app/job/${activeJobId}`),
            badge: "Active",
          },
        ]
      : []),
  ];

  const comingSoonLinks = [
    {
      label: "Sorting History",
      to: APP_ROUTES.HISTORY,
      icon: History,
      active: location.pathname === APP_ROUTES.HISTORY,
    },
    {
      label: "Analytics & Volume",
      to: APP_ROUTES.ANALYTICS,
      icon: BarChart3,
      active: location.pathname === APP_ROUTES.ANALYTICS,
    },
    {
      label: "Settings & Rules",
      to: APP_ROUTES.SETTINGS,
      icon: Settings,
      active: location.pathname === APP_ROUTES.SETTINGS,
    },
    {
      label: "API Access",
      to: APP_ROUTES.API_DOCS,
      icon: Code2,
      active: location.pathname === APP_ROUTES.API_DOCS,
    },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 z-40 bg-slate-950/60 backdrop-blur-sm lg:hidden animate-in fade-in"
          onClick={onCloseMobile}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={cn(
          "fixed top-0 bottom-0 left-0 z-50 flex flex-col w-72 bg-card border-r border-border/70 transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:z-0 shrink-0",
          isOpenMobile ? "translate-x-0 shadow-2xl" : "-translate-x-full"
        )}
      >
        {/* Mobile Header */}
        <div className="flex h-16 items-center justify-between px-6 border-b border-border/60 lg:hidden">
          <Link
            to={APP_ROUTES.HOME}
            onClick={onCloseMobile}
            className="flex items-center gap-2"
          >
            <div className="h-8 w-8 rounded-xl bg-primary flex items-center justify-center text-white font-bold">
              <Layers className="h-4 w-4" />
            </div>
            <span className="font-bold text-foreground">LabelSort Pro</span>
          </Link>
          <button
            onClick={onCloseMobile}
            className="p-1.5 rounded-lg text-muted-foreground hover:bg-muted"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* CTA Button */}
        <div className="p-4 pt-6">
          <Link to={APP_ROUTES.UPLOAD} onClick={onCloseMobile}>
            <Button
              variant="glow"
              size="lg"
              className="w-full justify-between group shadow-md"
              leftIcon={<UploadCloud className="h-5 w-5" />}
              rightIcon={<ArrowRight className="h-4 w-4 group-hover:translate-x-0.5 transition-transform" />}
            >
              Upload Labels
            </Button>
          </Link>
        </div>

        {/* Navigation Items */}
        <div className="flex-1 overflow-y-auto px-4 py-2 space-y-6">
          {/* Main Actions */}
          <div className="space-y-1">
            <p className="px-3 text-[11px] font-bold uppercase tracking-wider text-muted-foreground/70">
              Workspace
            </p>
            {mainLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={onCloseMobile}
                  className={cn(
                    "flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all group",
                    link.active
                      ? "bg-primary/10 text-primary font-semibold"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/60"
                  )}
                >
                  <div className="flex items-center gap-3">
                    <Icon
                      className={cn(
                        "h-4 w-4 transition-colors",
                        link.active ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
                      )}
                    />
                    <span>{link.label}</span>
                  </div>
                  {link.badge && (
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-primary text-white">
                      {link.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </div>

          {/* Coming Soon Section */}
          <div className="space-y-1">
            <div className="flex items-center justify-between px-3">
              <p className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground/70">
                Roadmap
              </p>
            </div>

            {comingSoonLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={onCloseMobile}
                  className={cn(
                    "flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all group",
                    link.active
                      ? "bg-secondary text-foreground font-semibold"
                      : "text-muted-foreground/80 hover:text-foreground hover:bg-muted/40"
                  )}
                >
                  <div className="flex items-center gap-3">
                    <Icon className="h-4 w-4 text-muted-foreground/60 group-hover:text-muted-foreground" />
                    <span>{link.label}</span>
                  </div>
                  <ComingSoonBadge />
                </Link>
              );
            })}
          </div>
        </div>

        {/* Server & Environment Footer */}
        <div className="p-4 border-t border-border/60 bg-muted/20">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-2">
              <span
                className={cn(
                  "h-2 w-2 rounded-full",
                  serverOnline ? "bg-emerald-500" : "bg-rose-500"
                )}
              />
              <span className="font-medium">
                {serverOnline ? "Backend Connected" : "Backend Offline"}
              </span>
            </div>
            <span className="font-mono text-[11px] opacity-70">v1.0.0</span>
          </div>
        </div>
      </aside>
    </>
  );
}
