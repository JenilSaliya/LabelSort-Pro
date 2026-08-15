from pathlib import Path

import pymupdf

from app.models.label import Label, LabelFields
from app.models.sort_options import SortOptions
from app.services.output.pdf_sorting_service import PDFSortingService


TEMP_DIR = Path("temp/test_output/pdf_sorting_service")
INPUT_PDF = TEMP_DIR / "input.pdf"
OUTPUT_PDF = TEMP_DIR / "sorted.pdf"


def build_label(
    label_id: str,
    page: int,
    sku: str,
) -> Label:
    return Label(
        id=label_id,
        pages=[page],
        fields=LabelFields(
            courier_partner="Valmo",
            payment_type="COD",
            tracking_number=f"TRACK-{page}",
            sku=sku,
            product_name="Test Product",
            size="6-7 Years",
            quantity=1,
            color="NA",
            order_number=f"ORDER-{page}",
            invoice_number=f"INV-{page}",
            order_date="27.07.2026",
        ),
    )


def create_test_pdf() -> None:
    """
    Create a simple 3-page PDF used by the integration test.
    """

    TEMP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    document = pymupdf.open()

    for page_number in range(1, 4):
        page = document.new_page()

        page.insert_text(
            (72, 72),
            f"ORIGINAL PAGE {page_number}",
        )

    document.save(INPUT_PDF)
    document.close()


def get_page_text(pdf_path: Path) -> list[str]:
    document = pymupdf.open(pdf_path)

    try:
        return [
            page.get_text("text").strip()
            for page in document
        ]
    finally:
        document.close()


def main() -> None:

    print("=" * 70)
    print("PDF SORTING SERVICE TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # CREATE TEST PDF
    # ------------------------------------------------------------

    create_test_pdf()

    print()
    print("INPUT PDF:")
    print(INPUT_PDF)

    # ------------------------------------------------------------
    # BUILD LABELS
    #
    # Physical PDF:
    #
    # page 1 -> SKU-C
    # page 2 -> SKU-A
    # page 3 -> SKU-B
    #
    # Expected sorted order:
    #
    # page 2 -> SKU-A
    # page 3 -> SKU-B
    # page 1 -> SKU-C
    # ------------------------------------------------------------

    labels = [
        build_label("label-c", 1, "SKU-C"),
        build_label("label-a", 2, "SKU-A"),
        build_label("label-b", 3, "SKU-B"),
    ]

    original_ids = [
        label.id
        for label in labels
    ]

    options = SortOptions(
        fields=["sku"],
    )

    # ------------------------------------------------------------
    # RUN PDF SORTING SERVICE
    # ------------------------------------------------------------

    service = PDFSortingService()

    result = service.sort_pdf(
        input_pdf=INPUT_PDF,
        output_pdf=OUTPUT_PDF,
        labels=labels,
        options=options,
    )

    print()
    print("OUTPUT PDF:")
    print(result)

    # ------------------------------------------------------------
    # VERIFY OUTPUT EXISTS
    # ------------------------------------------------------------

    assert OUTPUT_PDF.exists(), (
        "Output PDF was not created."
    )

    print("PASS: Output PDF created.")

    # ------------------------------------------------------------
    # VERIFY PAGE ORDER
    # ------------------------------------------------------------

    page_text = get_page_text(OUTPUT_PDF)

    print()
    print("OUTPUT PAGE ORDER:")

    for index, text in enumerate(page_text, start=1):
        print(
            f"output page {index}: {text}"
        )

    expected_order = [
        "ORIGINAL PAGE 2",
        "ORIGINAL PAGE 3",
        "ORIGINAL PAGE 1",
    ]

    assert page_text == expected_order, (
        f"Incorrect PDF page order.\n"
        f"Expected: {expected_order}\n"
        f"Actual:   {page_text}"
    )

    print("PASS: PDF pages sorted correctly.")

    # ------------------------------------------------------------
    # VERIFY PAGE COUNT
    # ------------------------------------------------------------

    document = pymupdf.open(OUTPUT_PDF)

    try:
        assert len(document) == 3
    finally:
        document.close()

    print("PASS: Correct page count.")

    # ------------------------------------------------------------
    # VERIFY ORIGINAL LABEL LIST
    # ------------------------------------------------------------

    assert [
        label.id
        for label in labels
    ] == original_ids

    print("PASS: Original label list preserved.")

    # ------------------------------------------------------------
    # FINAL
    # ------------------------------------------------------------

    print()
    print("=" * 70)
    print("PDF SORTING SERVICE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()