from pathlib import Path

from pypdf import PdfReader


class PDFInspectionService:
    """
    Inspects the technical structure of an uploaded PDF.

    This service does not perform sorting or Meesho-specific
    field extraction. It only analyzes the PDF structure.
    """

    def inspect_pdf(self, pdf_path: Path) -> dict:
        """
        Inspect a PDF and return page-level information.
        """

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        reader = PdfReader(pdf_path)

        pages = []
        text_pages = 0
        empty_pages = 0

        for index, page in enumerate(reader.pages):

            page_number = index + 1

            # Page dimensions
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)

            # Page rotation
            rotation = page.get("/Rotate", 0)

            # Extract text
            text = page.extract_text() or ""

            text_length = len(text.strip())

            if text_length > 0:
                text_pages += 1
            else:
                empty_pages += 1

            pages.append(
                {
                    "page_number": page_number,
                    "width": width,
                    "height": height,
                    "rotation": rotation,
                    "has_text": text_length > 0,
                    "text_length": text_length,
                    "text_preview": text.strip()[:500],
                }
            )

        return {
            "page_count": len(reader.pages),
            "text_pages": text_pages,
            "empty_pages": empty_pages,
            "pages": pages,
        }

    
    
    def inspect_page_coordinates(
        self,
        pdf_path: Path,
        page_number: int,
    ) -> dict:
        """
        Inspect text fragments and their coordinates on one PDF page.

        page_number is 1-based.
        """

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        reader = PdfReader(pdf_path)

        if page_number < 1 or page_number > len(reader.pages):
            raise ValueError(
                f"Invalid page number: {page_number}"
            )

        page = reader.pages[page_number - 1]

        fragments = []

        def visitor_text(
            text,
            cm,
            tm,
            font_dict,
            font_size,
        ):
            cleaned = text.strip()

            if not cleaned:
                return

            x = float(tm[4])
            y = float(tm[5])

            fragments.append(
                {
                    "text": cleaned,
                    "x": round(x, 2),
                    "y": round(y, 2),
                    "font_size": round(float(font_size), 2),
                }
            )

        page.extract_text(visitor_text=visitor_text)

        return {
            "page_number": page_number,
            "width": float(page.mediabox.width),
            "height": float(page.mediabox.height),
            "rotation": page.get("/Rotate", 0),
            "fragment_count": len(fragments),
            "fragments": fragments,
        }