import React, { useState, useEffect } from "react";
import { Outlet, useLocation, useParams } from "react-router-dom";
import { Topbar } from "./Topbar";
import { Sidebar } from "./Sidebar";
import { labelsortApi } from "@/features/labelsort/api/labelsortApi";
import { cn } from "@/lib/utils";

export function AppShell() {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [serverOnline, setServerOnline] = useState(true);
  const location = useLocation();
  const params = useParams<{ jobId?: string }>();

  // Full-width sorting layout (hide sidebar on desktop for spacious sorting workspace)
  const isSortingPage = location.pathname.endsWith("/sort") || location.pathname.includes("/sort");

  // Check if there is an active job from route params or sessionStorage
  const [activeJobId, setActiveJobId] = useState<string | null>(() => {
    return params.jobId || sessionStorage.getItem("labelsort_active_job_id") || null;
  });

  useEffect(() => {
    if (params.jobId) {
      setActiveJobId(params.jobId);
      sessionStorage.setItem("labelsort_active_job_id", params.jobId);
    }
  }, [params.jobId]);

  // Check health on mount
  useEffect(() => {
    let isMounted = true;
    labelsortApi
      .healthCheck()
      .then(() => {
        if (isMounted) setServerOnline(true);
      })
      .catch(() => {
        if (isMounted) setServerOnline(false);
      });
    return () => {
      isMounted = false;
    };
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground selection:bg-primary/20 selection:text-primary">
      <Topbar
        onToggleMobileSidebar={() => setMobileSidebarOpen((prev) => !prev)}
        activeJobId={activeJobId}
      />

      <div className="flex-1 flex w-full">
        {!isSortingPage && (
          <Sidebar
            activeJobId={activeJobId}
            isOpenMobile={mobileSidebarOpen}
            onCloseMobile={() => setMobileSidebarOpen(false)}
            serverOnline={serverOnline}
          />
        )}

        <main
          className={cn(
            "flex-1 flex flex-col min-w-0 bg-background/50 px-3 sm:px-6 md:px-8 py-4 sm:py-6 w-full",
            isSortingPage ? "max-w-[1400px] mx-auto" : "max-w-7xl mx-auto"
          )}
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}
