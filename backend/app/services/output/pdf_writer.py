from pathlib import Path

from pypdf import PdfReader, PdfWriter


class PDFWriter:
    """
    Creates a new PDF using a supplied page order.

    The page order is zero-independent / human page numbering:
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

        reader = PdfReader(str(input_path))
        writer = PdfWriter()

        total_pages = len(reader.pages)

        for page_number in page_order:

            if page_number < 1 or page_number > total_pages:
                raise ValueError(
                    f"Invalid page number {page_number}. "
                    f"PDF contains {total_pages} pages."
                )

            page_index = page_number - 1

            writer.add_page(
                reader.pages[page_index]
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open("wb") as output_file:
            writer.write(output_file)

        return output_path