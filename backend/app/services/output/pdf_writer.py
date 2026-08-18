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

    The page order uses human page numbering:
    page 1 means the first page of the PDF.
    """

    def write(
        self,
        input_pdf: str | Path,
        output_pdf: str | Path,
        page_order: list[int],
    ) -> Path:
        """
        Create a new PDF containing pages in the requested order.

        Example:

            page_order = [2, 1, 3]

        means:

            output page 1 = original page 2
            output page 2 = original page 1
            output page 3 = original page 3
        """

        input_path = Path(input_pdf)
        output_path = Path(output_pdf)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input PDF not found: {input_path}"
            )

        if not page_order:
            raise ValueError(
                "Page order cannot be empty."
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with pymupdf.open(str(input_path)) as source_doc:

            total_pages = len(source_doc)

            # Validate all page numbers before writing.
            for page_number in page_order:
                if page_number < 1 or page_number > total_pages:
                    raise ValueError(
                        f"Invalid page number {page_number}. "
                        f"PDF contains {total_pages} pages."
                    )

            # Create output document and insert pages
            # one at a time in the requested order.
            with pymupdf.open() as output_doc:

                for page_number in page_order:
                    page_index = page_number - 1
                    output_doc.insert_pdf(
                        source_doc,
                        from_page=page_index,
                        to_page=page_index,
                    )

                output_doc.save(str(output_path))

        logger.info(
            "Wrote %d pages to %s",
            len(page_order),
            output_path,
        )

        return output_path