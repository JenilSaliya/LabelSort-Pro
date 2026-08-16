import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../ui/Button";
import {
  ZoomIn,
  ZoomOut,
  RotateCw,
  ExternalLink,
  Download,
  Maximize2,
  FileText,
  SlidersHorizontal,
} from "lucide-react";
import { labelsortApi } from "@/features/labelsort/api/labelsortApi";
import { triggerBlobDownload } from "@/features/labelsort/utils/downloadUtils";
import { APP_ROUTES } from "@/lib/constants";
import { toast } from "sonner";

export interface PdfViewerProps {
  jobId: string;
  className?: string;
  showReSortButton?: boolean;
}

export function PdfViewer({ jobId, className, showReSortButton = true }: PdfViewerProps) {
  const [zoom, setZoom] = useState(100);
  const [rotation, setRotation] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  const previewUrl = labelsortApi.getPreviewUrl(jobId);

  const handleDownload = async () => {
    try {
      setIsDownloading(true);
      const blob = await labelsortApi.downloadSortedPdf(jobId);
      triggerBlobDownload(blob, `${jobId}_sorted_preview.pdf`);
      toast.success("PDF downloaded!");
    } catch (error: any) {
      toast.error(error.message || "Failed to download preview PDF.");
    } finally {
      setIsDownloading(false);
    }
  };

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 20, 200));
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 20, 60));
  const handleRotate = () => setRotation((prev) => (prev + 90) % 360);

  return (
    <div
      className={`flex flex-col rounded-2xl border border-border/80 bg-card overflow-hidden shadow-card ${
        isFullscreen ? "fixed inset-4 z-50 shadow-2xl" : ""
      } ${className || ""}`}
    >
      {/* Viewer Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2 px-3 sm:px-4 py-2.5 border-b border-border/60 bg-secondary/50 shrink-0">
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-primary" />
          <span className="text-xs font-bold text-foreground">
            PDF Preview
          </span>
        </div>

        {/* Controls */}
        <div className="flex flex-wrap items-center gap-1.5">
          {showReSortButton && (
            <Link to={APP_ROUTES.SORT(jobId)}>
              <Button
                variant="outline"
                size="sm"
                className="text-xs gap-1 h-8"
                leftIcon={<SlidersHorizontal className="h-3 w-3 text-primary" />}
              >
                Change Sorting Rules
              </Button>
            </Link>
          )}

          <div className="flex items-center">
            <button
              type="button"
              onClick={handleZoomOut}
              className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
              title="Zoom Out"
            >
              <ZoomOut className="h-4 w-4" />
            </button>
            <span className="font-mono text-xs text-muted-foreground px-1 select-none">
              {zoom}%
            </span>
            <button
              type="button"
              onClick={handleZoomIn}
              className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
              title="Zoom In"
            >
              <ZoomIn className="h-4 w-4" />
            </button>
          </div>

          <div className="h-4 w-px bg-border mx-0.5" />

          <button
            type="button"
            onClick={handleRotate}
            className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            title="Rotate 90°"
          >
            <RotateCw className="h-4 w-4" />
          </button>

          <button
            type="button"
            onClick={() => setIsFullscreen((prev) => !prev)}
            className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
          >
            <Maximize2 className="h-4 w-4" />
          </button>

          <a
            href={previewUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors flex items-center gap-1 text-xs"
            title="Open in new tab"
          >
            <ExternalLink className="h-4 w-4" />
          </a>

          <Button
            size="sm"
            variant="default"
            onClick={handleDownload}
            isLoading={isDownloading}
            className="h-8 text-xs"
            leftIcon={<Download className="h-3 w-3" />}
          >
            Download
          </Button>
        </div>
      </div>

      {/* Embed Container */}
      <div className="relative flex-1 bg-slate-900/10 dark:bg-slate-950 flex items-center justify-center overflow-auto p-2 sm:p-4 min-h-[400px]">
        <div
          className="w-full h-full min-h-[480px] flex items-center justify-center transition-transform duration-200"
          style={{
            transform: `scale(${zoom / 100}) rotate(${rotation}deg)`,
            transformOrigin: "center top",
          }}
        >
          <iframe
            src={`${previewUrl}#toolbar=0&navpanes=0`}
            title="PDF Preview"
            className="w-full h-[550px] rounded-xl border border-border/80 shadow-md bg-white"
          />
        </div>
      </div>
    </div>
  );
}
