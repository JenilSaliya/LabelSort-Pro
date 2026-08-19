from pathlib import Path
import pymupdf as fitz


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

        output_pdf.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with fitz.open() as merged_doc:
            for pdf_file in pdf_files:
                if not pdf_file.exists():
                    raise FileNotFoundError(
                        f"PDF file not found: {pdf_file}"
                    )

                with fitz.open(str(pdf_file)) as doc:
                    merged_doc.insert_pdf(doc)

            merged_doc.save(str(output_pdf))

        return output_pdf