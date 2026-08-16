import { useParams, useNavigate } from "react-router-dom";
import { PdfViewer } from "@/components/results/PdfViewer";
import { PageHeader } from "@/components/common/PageHeader";
import { Button } from "@/components/ui/Button";
import { APP_ROUTES } from "@/lib/constants";
import { ArrowLeft, CheckCircle2 } from "lucide-react";

export function PreviewPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();

  if (!jobId) {
    navigate(APP_ROUTES.UPLOAD);
    return null;
  }

  return (
    <div className="space-y-4 max-w-6xl mx-auto animate-in fade-in duration-200">
      <PageHeader
        title="Full Screen PDF Inspection"
        description="Inspect high-resolution vector barcodes, address sections, and SKU layout before sending to printer."
        actions={
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate(APP_ROUTES.RESULT(jobId))}
            leftIcon={<ArrowLeft className="h-4 w-4" />}
          >
            Back to Results
          </Button>
        }
      />

      <PdfViewer jobId={jobId} className="min-h-[75vh]" />
    </div>
  );
}
