from pathlib import Path

from app.models.label import Label
from app.models.sort_options import SortOptions
from app.services.sorting.sorting_service import SortingService
from app.services.output.page_order import PageOrderBuilder
from app.services.output.pdf_writer import PDFWriter


class LabelSortPipeline:
    """
    High-level orchestration service for LabelSort Pro.

    Connects:

        Labels
            ↓
        SortingService
            ↓
        PageOrderBuilder
            ↓
        PDFWriter

    The pipeline does not contain sorting logic itself.
    It coordinates the existing services.
    """

    def __init__(self) -> None:
        self.sorting_service = SortingService()
        self.page_order_builder = PageOrderBuilder()
        self.pdf_writer = PDFWriter()

    def sort_labels(
        self,
        labels: list[Label],
        options: SortOptions,
        input_pdf: str | Path,
        output_pdf: str | Path,
    ) -> Path:
        """
        Sort labels and create the reordered PDF.

        Parameters
        ----------
        labels:
            Parsed logical shipping labels.

        options:
            Sorting configuration.

        input_pdf:
            Original PDF.

        output_pdf:
            Destination for the sorted PDF.

        Returns
        -------
        Path
            Path to the generated sorted PDF.
        """

        if not labels:
            raise ValueError(
                "Cannot process an empty label list."
            )

        # --------------------------------------------------
        # STEP 1 - SORT LABELS
        # --------------------------------------------------

        sorted_labels = self.sorting_service.sort_labels(
            labels,
            options,
        )

        # --------------------------------------------------
        # STEP 2 - BUILD PHYSICAL PAGE ORDER
        # --------------------------------------------------

        page_order = self.page_order_builder.build(
            sorted_labels
        )

        # --------------------------------------------------
        # STEP 3 - WRITE OUTPUT PDF
        # --------------------------------------------------

        output_path = self.pdf_writer.write(
            input_pdf=input_pdf,
            output_pdf=output_pdf,
            page_order=page_order,
        )

        return output_path