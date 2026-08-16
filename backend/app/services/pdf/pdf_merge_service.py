from pathlib import Path

from pypdf import PdfReader, PdfWriter


class PdfMergeService:

    def merge(
        self,
        pdf_files: list[Path],
        output_pdf: Path,
    ) -> Path:

        if not pdf_files:
            raise ValueError(
                "No PDF files provided for merging."
            )

        writer = PdfWriter()

        for pdf_file in pdf_files:

            if not pdf_file.exists():
                raise FileNotFoundError(
                    f"PDF file not found: {pdf_file}"
                )

            reader = PdfReader(pdf_file)

            for page in reader.pages:
                writer.add_page(page)

        output_pdf.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_pdf.open("wb") as f:
            writer.write(f)

        return output_pdf