import React, { useState } from "react";
import { Button } from "../ui/Button";
import { Download, FileSpreadsheet, FileText, Eye, Check, SlidersHorizontal } from "lucide-react";
import { labelsortApi } from "@/features/labelsort/api/labelsortApi";
import { triggerBlobDownload } from "@/features/labelsort/utils/downloadUtils";
import { toast } from "sonner";
import { Link } from "react-router-dom";
import { APP_ROUTES } from "@/lib/constants";

export interface DownloadActionsProps {
  jobId: string;
  onOpenPreview?: () => void;
  showExcel?: boolean;
}

export function DownloadActions({
  jobId,
  onOpenPreview,
  showExcel = true,
}: DownloadActionsProps) {
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [downloadingExcel, setDownloadingExcel] = useState(false);
  const [pdfDownloaded, setPdfDownloaded] = useState(false);
  const [excelDownloaded, setExcelDownloaded] = useState(false);

  const handleDownloadPdf = async () => {
    try {
      setDownloadingPdf(true);
      const blob = await labelsortApi.downloadSortedPdf(jobId);
      triggerBlobDownload(blob, `${jobId}_sorted_labels.pdf`);
      setPdfDownloaded(true);
      toast.success("Sorted PDF downloaded!");
      setTimeout(() => setPdfDownloaded(false), 4000);
    } catch (error: any) {
      toast.error(error.message || "Failed to download sorted PDF.");
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleDownloadExcel = async () => {
    try {
      setDownloadingExcel(true);
      const blob = await labelsortApi.downloadStatistics(jobId);
      triggerBlobDownload(blob, `${jobId}_statistics.xlsx`);
      setExcelDownloaded(true);
      toast.success("Excel spreadsheet downloaded!");
      setTimeout(() => setExcelDownloaded(false), 4000);
    } catch (error: any) {
      toast.error(error.message || "Failed to download Excel statistics.");
    } finally {
      setDownloadingExcel(false);
    }
  };

  return (
    <div
      className={`grid gap-4 ${
        showExcel ? "grid-cols-1 md:grid-cols-2" : "grid-cols-1 max-w-xl mx-auto w-full"
      }`}
    >
      {/* PDF Download Card */}
      <div className="p-5 sm:p-6 rounded-2xl border border-primary/20 bg-primary/5 dark:bg-primary/10 flex flex-col justify-between space-y-4 shadow-sm">
        <div className="flex items-start gap-3.5">
          <div className="p-3 rounded-xl bg-primary text-white shrink-0 shadow-md shadow-primary/20">
            <FileText className="h-6 w-6" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h4 className="text-base font-bold text-foreground truncate">
                Sorted PDF Ready
              </h4>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 shrink-0">
                Print Ready
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed">
              Organized by your selected courier & SKU criteria.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 pt-2">
          <Button
            variant="glow"
            size="lg"
            className="flex-1 shadow-sm text-sm"
            onClick={handleDownloadPdf}
            isLoading={downloadingPdf}
            leftIcon={
              pdfDownloaded ? (
                <Check className="h-4 w-4 text-emerald-300" />
              ) : (
                <Download className="h-4 w-4" />
              )
            }
          >
            {pdfDownloaded ? "Downloaded" : "Download Sorted PDF"}
          </Button>

          {onOpenPreview && (
            <Button
              variant="outline"
              size="lg"
              onClick={onOpenPreview}
              title="Preview PDF"
              className="sm:w-auto text-sm"
              leftIcon={<Eye className="h-4 w-4" />}
            >
              Preview Map
            </Button>
          )}
        </div>
      </div>

      {/* Excel Download Card (shown if enabled) */}
      {showExcel && (
        <div className="p-5 sm:p-6 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 dark:bg-emerald-500/10 flex flex-col justify-between space-y-4 shadow-sm">
          <div className="flex items-start gap-3.5">
            <div className="p-3 rounded-xl bg-emerald-600 text-white shrink-0 shadow-md shadow-emerald-600/20">
              <FileSpreadsheet className="h-6 w-6" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h4 className="text-base font-bold text-foreground truncate">
                  Statistics Excel File
                </h4>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 shrink-0">
                  .xlsx
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed">
                Full breakdown of SKU inventory and courier distribution.
              </p>
            </div>
          </div>

          <div className="pt-2">
            <Button
              variant="success"
              size="lg"
              className="w-full shadow-sm text-sm"
              onClick={handleDownloadExcel}
              isLoading={downloadingExcel}
              leftIcon={
                excelDownloaded ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Download className="h-4 w-4" />
                )
              }
            >
              {excelDownloaded ? "Downloaded" : "Download Excel Report"}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
