import logging
from pathlib import Path

import pymupdf

logger = logging.getLogger(__name__)


class PDFWriter:
    """
    Creates a new PDF using a supplied page order.

    Uses pymupdf (MuPDF) for page copying, which operates
    at the C level and uses significantly less Python heap
    memory than pypdf's PdfReader + PdfWriter approach.

    The page order uses 1-indexed human page numbering.
    """

    def write(
        self,
        input_pdf: str | Path,
        output_pdf: str | Path,
        page_order: list[int],
    ) -> Path:
        """
        Create a new PDF containing pages in the requested order with invariant checks.
        """
        input_path = Path(input_pdf)
        output_path = Path(output_pdf)

        if not input_path.exists():
            raise FileNotFoundError(f"Input PDF not found: {input_path}")

        if not page_order:
            raise ValueError("Page order cannot be empty.")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with pymupdf.open(str(input_path)) as doc:
            total_pages = len(doc)

            # Invariant 1: Total page count match
            if len(page_order) != total_pages:
                raise ValueError(
                    f"Page count mismatch in sorting: PDF has {total_pages} pages, "
                    f"but page order contains {len(page_order)} pages."
                )

            # Invariant 2: No duplicate pages
            if len(set(page_order)) != total_pages:
                raise ValueError("Duplicate page numbers detected in sorting order.")

            # Invariant 3: Validate page number boundaries
            for page_number in page_order:
                if page_number < 1 or page_number > total_pages:
                    raise ValueError(
                        f"Invalid page number {page_number}. PDF contains {total_pages} pages."
                    )

            # Reorder pages using PyMuPDF's C-level select method (instantaneous, minimal RAM)
            doc.select([page_number - 1 for page_number in page_order])
            doc.save(str(output_path), garbage=3, deflate=True)

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise RuntimeError(f"Failed to generate sorted output PDF at {output_path}")

        logger.info("Successfully wrote %d pages to %s (%d bytes)", len(page_order), output_path, output_path.stat().st_size)
        return output_path