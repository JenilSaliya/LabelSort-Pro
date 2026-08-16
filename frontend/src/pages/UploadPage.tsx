import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { FileList } from "@/components/upload/FileList";
import { UploadProgressCard } from "@/components/upload/UploadProgressCard";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { labelsortApi } from "@/features/labelsort/api/labelsortApi";
import { APP_ROUTES, MAX_UPLOAD_SIZE_BYTES, MAX_UPLOAD_SIZE_MB } from "@/lib/constants";
import { UploadCloud, ArrowRight, ShieldCheck, AlertCircle } from "lucide-react";
import { toast } from "sonner";

export function UploadPage() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStage, setUploadStage] = useState("Preparing files...");
  const [isDragOver, setIsDragOver] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const validateAndAddFiles = (fileList: FileList | File[]) => {
    setErrorMessage(null);
    const validFiles: File[] = [];
    const invalidFiles: string[] = [];

    Array.from(fileList).forEach((file) => {
      const isPdf =
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf");

      if (!isPdf) {
        invalidFiles.push(`${file.name} (Not a PDF)`);
        return;
      }

      if (file.size > MAX_UPLOAD_SIZE_BYTES) {
        invalidFiles.push(`${file.name} (Exceeds ${MAX_UPLOAD_SIZE_MB}MB limit)`);
        return;
      }

      validFiles.push(file);
    });

    if (invalidFiles.length > 0) {
      setErrorMessage(invalidFiles.join(", "));
      toast.error("Some files were not valid PDFs or exceeded size limits.");
    }

    if (validFiles.length > 0) {
      setSelectedFiles((prev) => {
        const existingNames = new Set(prev.map((f) => f.name));
        const nonDuplicates = validFiles.filter((f) => !existingNames.has(f.name));
        if (nonDuplicates.length < validFiles.length) {
          toast.info("Duplicate files were skipped.");
        }
        return [...prev, ...nonDuplicates];
      });
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (isUploading) return;
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (isUploading) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndAddFiles(e.dataTransfer.files);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndAddFiles(e.target.files);
      e.target.value = "";
    }
  };

  const handleRemoveFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleClearAll = () => {
    setSelectedFiles([]);
  };

  const openFilePicker = () => {
    if (!isUploading && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleUploadAndProcess = async () => {
    if (selectedFiles.length === 0) {
      toast.error("Please select at least one PDF file.");
      return;
    }

    try {
      setIsUploading(true);
      setUploadProgress(15);
      setUploadStage("Uploading labels to server...");

      const response = await labelsortApi.uploadFiles(
        selectedFiles,
        (percent) => {
          const calculated = Math.min(85, Math.max(15, percent));
          setUploadProgress(calculated);
          if (percent > 75) {
            setUploadStage("Extracting barcodes & SKU metadata...");
          }
        }
      );

      if (response.success && response.data?.job_id) {
        setUploadProgress(100);
        setUploadStage("Analysis ready! Loading sorting options...");
        const jobId = response.data.job_id;
        sessionStorage.setItem("labelsort_active_job_id", jobId);
        toast.success("Labels uploaded successfully!");

        setTimeout(() => {
          navigate(APP_ROUTES.SORT(jobId));
        }, 400);
      } else {
        throw new Error(response.message || "Failed to process uploaded labels.");
      }
    } catch (error: any) {
      setIsUploading(false);
      setUploadProgress(0);
      toast.error(error.message || "Upload failed. Please check backend connection.");
    }
  };

  return (
    <div className="space-y-4 max-w-xl mx-auto animate-in fade-in duration-200">
      {/* Hidden File Input mounted at all times */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,application/pdf"
        multiple
        onChange={handleInputChange}
        className="hidden"
        disabled={isUploading}
      />

      {/* Upload Card */}
      <Card
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`p-5 sm:p-7 border transition-all duration-200 shadow-card flex flex-col space-y-4 ${
          isDragOver
            ? "border-primary bg-primary/10 scale-[1.01] shadow-glow-primary"
            : "border-border/80"
        }`}
      >
        <div className="text-center space-y-1">
          <h2 className="text-xl sm:text-2xl font-extrabold text-foreground tracking-tight">
            Upload Shipping Labels
          </h2>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Upload your Meesho shipping label PDF to crop invoice space, sort labels, and prepare a cleaner print-ready file.
          </p>
        </div>

        {/* Dynamic Center Box: Shows Dropzone when 0 files, File List when >0 files, or Progress when uploading */}
        <div className="w-full">
          {isUploading ? (
            <UploadProgressCard
              progress={uploadProgress}
              fileCount={selectedFiles.length}
              stageText={uploadStage}
              isComplete={uploadProgress === 100}
            />
          ) : selectedFiles.length === 0 ? (
            <div
              onClick={openFilePicker}
              className="relative flex flex-col items-center justify-center p-6 sm:p-10 rounded-2xl border-2 border-dashed border-primary/40 dark:border-primary/30 hover:border-primary bg-primary/5 dark:bg-primary/[0.03] hover:bg-primary/[0.08] transition-all duration-200 cursor-pointer select-none text-center group"
            >
              <div className="p-4 rounded-2xl bg-primary/15 text-primary mb-3.5 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary group-hover:text-white shadow-sm">
                <UploadCloud className="h-7 w-7" />
              </div>

              <h3 className="text-sm sm:text-base font-bold text-foreground mb-1">
                <span className="text-primary hover:underline">Click here</span> to upload or Drag & Drop Meesho Label PDFs
              </h3>

              <p className="text-xs text-muted-foreground max-w-xs leading-relaxed mb-3">
                Supported format: PDF • Up to {MAX_UPLOAD_SIZE_MB}MB
              </p>
            </div>
          ) : (
            <FileList
              files={selectedFiles}
              onRemove={handleRemoveFile}
              onClearAll={handleClearAll}
              onAddMore={openFilePicker}
              disabled={isUploading}
            />
          )}
        </div>

        {errorMessage && (
          <div className="flex items-center gap-2 p-2.5 rounded-xl bg-destructive/10 text-destructive text-xs font-medium border border-destructive/20 animate-in fade-in">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span className="truncate">{errorMessage}</span>
          </div>
        )}

        {/* Action Button positioned directly below the box */}
        <div className="pt-1">
          <Button
            variant="glow"
            size="lg"
            className="w-full shadow-md text-sm sm:text-base py-3"
            disabled={selectedFiles.length === 0 || isUploading}
            onClick={handleUploadAndProcess}
            isLoading={isUploading}
            leftIcon={!isUploading ? <UploadCloud className="h-5 w-5" /> : undefined}
            rightIcon={!isUploading && selectedFiles.length > 0 ? <ArrowRight className="h-4 w-4" /> : undefined}
          >
            {isUploading
              ? `Uploading... ${uploadProgress}%`
              : selectedFiles.length > 0
              ? `Upload & Prepare Labels (${selectedFiles.length})`
              : "Upload & Prepare Labels"}
          </Button>
        </div>

        <div className="flex items-center justify-center gap-1.5 text-[11px] text-muted-foreground pt-1">
          <ShieldCheck className="h-3.5 w-3.5 text-emerald-500 shrink-0" />
          <span>Files processed in an isolated secure session</span>
        </div>
      </Card>
    </div>
  );
}
