from pathlib import Path

from app.models.label import Label
from app.models.sort_options import SortOptions
from app.services.output.page_order import PageOrderBuilder
from app.services.output.pdf_writer import PDFWriter
from app.services.sorting.sorting_service import SortingService


class PDFSortingService:
    """
    Coordinates the complete PDF sorting pipeline.

    Flow:

        Label objects
            ↓
        SortingService
            ↓
        PageOrderBuilder
            ↓
        PDFWriter
            ↓
        Sorted PDF
    """

    def __init__(
        self,
        sorting_service: SortingService | None = None,
        page_order_builder: PageOrderBuilder | None = None,
        pdf_writer: PDFWriter | None = None,
    ):
        self.sorting_service = (
            sorting_service
            or SortingService()
        )

        self.page_order_builder = (
            page_order_builder
            or PageOrderBuilder()
        )

        self.pdf_writer = (
            pdf_writer
            or PDFWriter()
        )

    def sort_pdf(
        self,
        input_pdf: str | Path,
        output_pdf: str | Path,
        labels: list[Label],
        options: SortOptions,
    ) -> Path:
        """
        Sort labels and create a physically reordered PDF.
        """

        if not labels:
            raise ValueError(
                "Cannot sort PDF without labels."
            )

        # --------------------------------------------------
        # STEP 1
        # Sort logical labels
        # --------------------------------------------------

        sorted_labels = self.sorting_service.sort_labels(
            labels,
            options,
        )

        # --------------------------------------------------
        # STEP 2
        # Convert sorted labels into PDF page order
        # --------------------------------------------------

        page_order = self.page_order_builder.build(
            sorted_labels
        )

        # --------------------------------------------------
        # STEP 3
        # Create the reordered PDF
        # --------------------------------------------------

        return self.pdf_writer.write(
            input_pdf=input_pdf,
            output_pdf=output_pdf,
            page_order=page_order,
        )