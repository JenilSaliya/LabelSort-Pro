import { Modal } from "../ui/Modal";
import { PdfViewer } from "./PdfViewer";

export interface PdfPreviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  jobId: string;
}

export function PdfPreviewModal({
  isOpen,
  onClose,
  jobId,
}: PdfPreviewModalProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Print-Ready PDF Preview"
      description="Inspect the final sorted shipping label layout before printing."
      maxWidth="4xl"
    >
      <PdfViewer jobId={jobId} className="w-full" />
    </Modal>
  );
}
