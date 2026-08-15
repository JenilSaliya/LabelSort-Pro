from app.models.label import Label, LabelFields
from app.services.sorting.sorter import LabelSorter


def build_label(
    label_id: str,
    pages: list[int],
    sku: str,
    product_name: str,
    color: str,
) -> Label:

    return Label(
        id=label_id,
        pages=pages,
        fields=LabelFields(
            courier_partner="Valmo",
            payment_type="COD",
            tracking_number=f"TRACK-{label_id}",
            sku=sku,
            product_name=product_name,
            size="6-7 Years",
            quantity=1,
            color=color,
            order_number=f"ORDER-{label_id}",
            invoice_number=f"INV-{label_id}",
            order_date="27.07.2026",
        ),
    )


def main():

    sorter = LabelSorter()

    print("=" * 70)
    print("SORTER - CASE-INSENSITIVE TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # TEST 1: SKU CASE
    # ------------------------------------------------------------

    labels = [
        build_label(
            "upper",
            [1],
            "SKU-C",
            "Product C",
            "Blue",
        ),
        build_label(
            "lower",
            [2],
            "sku-a",
            "Product A",
            "Red",
        ),
        build_label(
            "mixed",
            [3],
            "Sku-B",
            "Product B",
            "Green",
        ),
    ]

    sorted_labels = sorter.sort(
        labels,
        key="sku",
    )

    print("\nTEST 1 - SKU CASE")

    for label in sorted_labels:
        print(
            label.id,
            label.fields.sku,
        )

    assert [
        label.fields.sku
        for label in sorted_labels
    ] == [
        "sku-a",
        "Sku-B",
        "SKU-C",
    ]

    print("PASS: SKU sorting is case-insensitive.")

    # ------------------------------------------------------------
    # TEST 2: LEADING / TRAILING SPACES
    # ------------------------------------------------------------

    labels = [
        build_label(
            "b",
            [1],
            "  SKU-B  ",
            "Product B",
            "Blue",
        ),
        build_label(
            "a",
            [2],
            "SKU-A",
            "Product A",
            "Red",
        ),
        build_label(
            "c",
            [3],
            " sku-c ",
            "Product C",
            "Green",
        ),
    ]

    sorted_labels = sorter.sort(
        labels,
        key="sku",
    )

    print("\nTEST 2 - WHITESPACE")

    for label in sorted_labels:
        print(
            label.id,
            repr(label.fields.sku),
        )

    assert [
        label.fields.sku.strip().lower()
        for label in sorted_labels
    ] == [
        "sku-a",
        "sku-b",
        "sku-c",
    ]

    print("PASS: Leading/trailing whitespace handled.")

    # ------------------------------------------------------------
    # TEST 3: PRODUCT NAME CASE
    # ------------------------------------------------------------

    labels = [
        build_label(
            "c",
            [1],
            "SKU-C",
            "zebra product",
            "Blue",
        ),
        build_label(
            "a",
            [2],
            "SKU-A",
            "APPLE product",
            "Red",
        ),
        build_label(
            "b",
            [3],
            "SKU-B",
            "Banana product",
            "Green",
        ),
    ]

    sorted_labels = sorter.sort(
        labels,
        key="product_name",
    )

    print("\nTEST 3 - PRODUCT NAME CASE")

    for label in sorted_labels:
        print(
            label.id,
            label.fields.product_name,
        )

    assert [
        label.fields.product_name
        for label in sorted_labels
    ] == [
        "APPLE product",
        "Banana product",
        "zebra product",
    ]

    print("PASS: Product-name sorting is case-insensitive.")

    print("\n" + "=" * 70)
    print("ALL CASE-INSENSITIVE SORTING TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()