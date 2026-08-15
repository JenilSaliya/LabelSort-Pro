from pathlib import Path

from pypdf import PdfReader, PdfWriter

from app.services.output.pdf_writer import PDFWriter


def create_test_pdf(path: Path) -> None:
    """
    Create a simple 3-page PDF for testing.
    """

    writer = PdfWriter()

    for _ in range(3):
        writer.add_blank_page(
            width=595,
            height=842,
        )

    with path.open("wb") as file:
        writer.write(file)


def main():

    print("=" * 70)
    print("PDF WRITER TEST")
    print("=" * 70)

    test_directory = Path("temp/test_output")
    test_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    input_pdf = test_directory / "input.pdf"
    output_pdf = test_directory / "sorted.pdf"

    # ---------------------------------------------------------
    # Create test PDF
    # ---------------------------------------------------------

    create_test_pdf(input_pdf)

    print("\nINPUT PDF:")
    print(input_pdf)

    # ---------------------------------------------------------
    # Test page order
    # ---------------------------------------------------------

    page_order = [2, 3, 1]

    writer = PDFWriter()

    result = writer.write(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        page_order=page_order,
    )

    print("\nOUTPUT PDF:")
    print(result)

    # ---------------------------------------------------------
    # Validate
    # ---------------------------------------------------------

    assert output_pdf.exists()

    reader = PdfReader(str(output_pdf))

    assert len(reader.pages) == 3

    print("\nOUTPUT PAGE COUNT:")
    print(len(reader.pages))

    assert len(reader.pages) == 3

    print("\nPASS: PDF output created.")
    print("PASS: Correct page count.")
    print("PASS: Page reorder operation completed.")

    print("\n" + "=" * 70)
    print("PDF WRITER TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()