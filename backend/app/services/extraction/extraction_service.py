from typing import Callable, Optional
import pymupdf as fitz

from app.models.label import Label
from app.services.marketplace.detector import MarketplaceDetector
from app.services.meesho.parser import MeeshoParser
from app.services.meesho.label_builder import build_label


class ExtractionService:
    """
    Extracts structured shipping labels from PDF files.

    Completely decoupled from HTTP, framework, or queue implementations.
    Supports progress callbacks and memory bounding.
    """

    def __init__(self) -> None:
        self.marketplace_detector = MarketplaceDetector()
        self.meesho_parser = MeeshoParser()

    def extract_labels(
        self,
        input_pdf: str | fitz.Document,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> tuple[str, int, list[Label]]:
        """
        Extract labels from a PDF file.

        Parameters:
            input_pdf: Path to the PDF file or an open fitz.Document.
            on_progress: Optional callback invoked with (current_page, total_pages).

        Returns:
            tuple of (marketplace_name, total_page_count, list_of_labels)
        """
        labels: list[Label] = []

        # Support both path strings and pre-opened documents
        doc = fitz.open(str(input_pdf)) if isinstance(input_pdf, (str, bytes)) or hasattr(input_pdf, "resolve") else input_pdf

        try:
            page_count = len(doc)
            if page_count == 0:
                raise ValueError("The PDF document contains no pages.")

            # Detect marketplace from first page
            first_page_text = doc[0].get_text("text")
            marketplace = self.marketplace_detector.detect(first_page_text)

            if marketplace.value != "meesho":
                raise ValueError(
                    f"Unsupported marketplace: {marketplace.value}"
                )

            # Process pages
            for page_index in range(page_count):
                page_number = page_index + 1
                page = doc[page_index]

                text = page.get_text("text")

                # Free MuPDF decompression caches periodically to bound memory
                if page_number % 50 == 0:
                    fitz.TOOLS.store_shrink(100)

                # Report progress every 20 pages and on the final page
                if on_progress and (page_number % 20 == 0 or page_number == page_count):
                    on_progress(page_number, page_count)

                # Fast blank page check without string allocation
                if not text or text.isspace():
                    continue

                parsed = self.meesho_parser.parse_page(text, page_number)
                label = build_label(parsed)
                labels.append(label)

            # Final memory flush
            fitz.TOOLS.store_shrink(100)

            if not labels:
                raise ValueError("No valid shipping labels extracted from PDF.")

            return (
                marketplace.value,
                page_count,
                labels,
            )

        finally:
            if doc is not input_pdf and hasattr(doc, "close"):
                doc.close()