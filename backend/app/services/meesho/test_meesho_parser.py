from pathlib import Path

import pymupdf

from app.services.meesho.parser import MeeshoParser


PDF_PATH = Path(
    r"F:\Jenil\project\labelsort-pro\backend"
    r"\temp\jobs\20260810_194508_664d4b"
    r"\original\original.pdf"
)


def print_result(result: dict) -> None:
    print()
    print("=" * 70)
    print(f"PAGE {result['page_number']}")
    print("=" * 70)

    for key, value in result.items():
        print(f"{key:20}: {value}")


def validate_result(result: dict) -> None:
    """
    Basic structural validation.

    These checks verify that the parser is actually extracting
    the fields we need.

    We do not hardcode every page's exact values here yet.
    That belongs in the full parser test stage.
    """

    required_keys = {
        "page_number",
        "courier_partner",
        "payment_type",
        "tracking_number",
        "sku",
        "product_name",
        "size",
        "quantity",
        "color",
        "order_number",
        "invoice_number",
        "order_date",
    }

    missing_keys = required_keys - set(result.keys())

    assert not missing_keys, (
        f"Missing parser fields: {sorted(missing_keys)}"
    )

    assert isinstance(
        result["page_number"],
        int,
    )

    assert result["courier_partner"] is not None, (
        f"Courier not detected on page "
        f"{result['page_number']}"
    )

    assert result["payment_type"] in {
        "COD",
        "Prepaid",
        None,
    }, (
        f"Invalid payment type on page "
        f"{result['page_number']}: {result['payment_type']}"
    )

    assert result["tracking_number"], (
        f"Tracking number not detected on page "
        f"{result['page_number']}"
    )

    assert result["sku"], (
        f"SKU not detected on page "
        f"{result['page_number']}"
    )

    assert result["size"], (
        f"Size not detected on page "
        f"{result['page_number']}"
    )

    assert result["quantity"] is not None, (
        f"Quantity not detected on page "
        f"{result['page_number']}"
    )

    assert result["color"], (
        f"Color not detected on page "
        f"{result['page_number']}"
    )

    assert result["order_number"], (
        f"Order number not detected on page "
        f"{result['page_number']}"
    )

    assert result["invoice_number"], (
        f"Invoice number not detected on page "
        f"{result['page_number']}"
    )

    assert result["order_date"], (
        f"Order date not detected on page "
        f"{result['page_number']}"
    )


def main() -> None:
    print("=" * 70)
    print("MEESHO PARSER - 15 PAGE TEST")
    print("=" * 70)

    print()
    print(f"PDF: {PDF_PATH}")

    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"Test PDF not found:\n{PDF_PATH}"
        )

    parser = MeeshoParser()

    document = pymupdf.open(PDF_PATH)

    results = []

    try:
        print()
        print(f"TOTAL PDF PAGES: {len(document)}")

        for page_index in range(len(document)):

            page_number = page_index + 1

            page = document[page_index]

            text = page.get_text("text")

            if not text.strip():
                raise AssertionError(
                    f"Page {page_number} contains no text."
                )

            result = parser.parse_page(
                text,
                page_number=page_number,
            )

            # print_result(result)

            validate_result(result)

            results.append(result)

            print_result(result)

        print()
        print("=" * 70)
        print("PARSER TEST PASSED")
        print("=" * 70)

        print()
        print(f"Pages tested : {len(results)}")
        print("All required fields detected.")

    finally:
        document.close()


if __name__ == "__main__":
    main()