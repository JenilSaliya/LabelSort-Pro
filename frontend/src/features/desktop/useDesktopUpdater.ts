import { useEffect } from "react";
import { toast } from "sonner";

export function useDesktopUpdater() {
  useEffect(() => {
    // Only execute when running in Tauri Desktop environment
    const isDesktop =
      typeof window !== "undefined" &&
      ("__TAURI_INTERNALS__" in window || (window as any).__LABELSORT_PORT__);

    if (!isDesktop) return;

    let isMounted = true;

    async function checkForUpdates() {
      try {
        // Dynamically import Tauri updater and process plugins
        const { check } = await import("@tauri-apps/plugin-updater");
        const { relaunch } = await import("@tauri-apps/plugin-process");

        const update = await check();

        if (update && update.available && isMounted) {
          console.log(`[AutoUpdater] New update found: v${update.version}`);
          
          toast.info(`Updating LabelSort Pro to v${update.version}...`, {
            description: "Downloading update in the background.",
            duration: 5000,
          });

          // Download and apply the update
          await update.downloadAndInstall();

          if (isMounted) {
            toast.success(`🎉 LabelSort Pro v${update.version} is ready!`, {
              description: "Restart the application now to apply the update.",
              action: {
                label: "Restart Now",
                onClick: async () => {
                  await relaunch();
                },
              },
              duration: 30000,
            });
          }
        }
      } catch (err) {
        // Silently log in development/offline modes
        console.debug("[AutoUpdater] Update check skipped or offline:", err);
      }
    }

    // Run check 3 seconds after startup so UI loads immediately
    const timer = setTimeout(() => {
      checkForUpdates();
    }, 3000);

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, []);
}
