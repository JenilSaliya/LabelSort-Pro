from pathlib import Path

import pymupdf

from app.services.meesho.parser import MeeshoParser


PDF_PATH = Path(
    r"F:\Jenil\project\labelsort-pro\backend\temp\jobs\20260810_194508_664d4b\original\original.pdf"
)


def main():
    parser = MeeshoParser()

    document = pymupdf.open(PDF_PATH)

    try:
        results = []

        for page_index in range(len(document)):
            page = document[page_index]

            text = page.get_text("text")

            result = parser.parse_page(
                text,
                page_number=page_index + 1,
            )

            results.append(result)

        for result in results:
            print()
            print("=" * 70)
            print(f"PAGE {result['page_number']}")
            print("=" * 70)

            print(
                f"{'page_number':20}: "
                f"{result['page_number']}"
            )

            print(
                f"{'courier_partner':20}: "
                f"{result['courier_partner']}"
            )

            print(
                f"{'payment_type':20}: "
                f"{result['payment_type']}"
            )

            print(
                f"{'tracking_number':20}: "
                f"{result['tracking_number']}"
            )

            print(
                f"{'sku':20}: "
                f"{result['sku']}"
            )

            print(
                f"{'product_name':20}: "
                f"{result['product_name']}"
            )

            print(
                f"{'size':20}: "
                f"{result['size']}"
            )

            print(
                f"{'quantity':20}: "
                f"{result['quantity']}"
            )

            print(
                f"{'color':20}: "
                f"{result['color']}"
            )

            print(
                f"{'order_number':20}: "
                f"{result['order_number']}"
            )

            print(
                f"{'invoice_number':20}: "
                f"{result['invoice_number']}"
            )

            print(
                f"{'order_date':20}: "
                f"{result['order_date']}"
            )

        print()
        print("=" * 70)
        print(f"TOTAL PAGES: {len(results)}")
        print("=" * 70)

    finally:
        document.close()


if __name__ == "__main__":
    main()