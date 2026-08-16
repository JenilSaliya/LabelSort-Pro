import { Link } from "react-router-dom";
import { ThemeToggle } from "./ThemeToggle";
import { Layers, Menu, Sparkles, HelpCircle, ExternalLink } from "lucide-react";
import { Badge } from "../ui/Badge";
import { APP_ROUTES } from "@/lib/constants";

export interface TopbarProps {
  onToggleMobileSidebar?: () => void;
  activeJobId?: string | null;
}

export function Topbar({ onToggleMobileSidebar, activeJobId }: TopbarProps) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/70 bg-card/85 backdrop-blur-md transition-colors">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        {/* Left branding & mobile trigger */}
        <div className="flex items-center gap-3">
          {onToggleMobileSidebar && (
            <button
              onClick={onToggleMobileSidebar}
              className="lg:hidden p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors border border-border/40"
              aria-label="Toggle navigation menu"
            >
              <Menu className="h-5 w-5" />
            </button>
          )}

          <Link
            to={APP_ROUTES.HOME}
            className="flex items-center gap-2.5 group focus-visible:outline-none"
          >
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-primary to-indigo-500 flex items-center justify-center text-white shadow-md shadow-primary/20 group-hover:scale-105 transition-transform">
              <Layers className="h-5 w-5" />
            </div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-lg sm:text-xl tracking-tight text-foreground">
                Label<span className="text-primary">Sort</span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                PRO
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Active Job Status Pill (if present) */}
        {activeJobId && (
          <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/80 border border-border/60 text-xs text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Active Session:</span>
            <Link
              to={APP_ROUTES.SORT(activeJobId)}
              className="font-mono font-medium text-foreground hover:text-primary transition-colors truncate max-w-[150px]"
            >
              {activeJobId}
            </Link>
          </div>
        )}

        {/* Right tools */}
        <div className="flex items-center gap-2.5">
          <Badge
            variant="secondary"
            className="hidden sm:inline-flex bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20 text-xs py-1"
          >
            <Sparkles className="h-3 w-3 mr-1 inline-block" />
            Meesho Active
          </Badge>

          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground p-2 rounded-xl hover:bg-muted/60 transition-colors"
          >
            <HelpCircle className="h-4 w-4" />
            <span>Docs</span>
            <ExternalLink className="h-3 w-3 opacity-60" />
          </a>

          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
