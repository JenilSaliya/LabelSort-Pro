from app.models.label import Label, LabelFields
from app.services.sorting.sorter import LabelSorter


def build_label(
    label_id: str,
    pages: list[int],
    sku: str | None,
    quantity: int | None,
    color: str | None,
) -> Label:

    return Label(
        id=label_id,
        pages=pages,
        fields=LabelFields(
            courier_partner="Valmo",
            payment_type="COD",
            tracking_number=f"TRACK-{label_id}",
            sku=sku,
            product_name="Test Product",
            size="6-7 Years",
            quantity=quantity,
            color=color,
            order_number=f"ORDER-{label_id}",
            invoice_number=f"INV-{label_id}",
            order_date="27.07.2026",
        ),
    )


def main():

    sorter = LabelSorter()

    print("=" * 70)
    print("SORTER - MISSING VALUE TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # TEST 1: MISSING SKU
    # ------------------------------------------------------------

    labels = [
        build_label("sku-b", [1], "SKU-B", 2, "Blue"),
        build_label("missing", [2], None, 1, "Red"),
        build_label("sku-a", [3], "SKU-A", 3, "Green"),
    ]

    sorted_labels = sorter.sort(
        labels,
        key="sku",
    )

    print("\nTEST 1 - MISSING SKU")

    for label in sorted_labels:
        print(
            label.id,
            "SKU:",
            label.fields.sku,
        )

    assert sorted_labels[0].fields.sku is None
    assert sorted_labels[1].fields.sku == "SKU-A"
    assert sorted_labels[2].fields.sku == "SKU-B"

    print("PASS: Missing SKU handled safely.")

    # ------------------------------------------------------------
    # TEST 2: MISSING COLOR
    # ------------------------------------------------------------

    labels = [
        build_label("color-b", [1], "SKU-B", 1, "Blue"),
        build_label("missing", [2], "SKU-C", 2, None),
        build_label("color-a", [3], "SKU-A", 3, "Green"),
    ]

    sorted_labels = sorter.sort(
        labels,
        key="color",
    )

    print("\nTEST 2 - MISSING COLOR")

    for label in sorted_labels:
        print(
            label.id,
            "COLOR:",
            label.fields.color,
        )

    assert sorted_labels[0].fields.color is None
    assert sorted_labels[1].fields.color == "Blue"
    assert sorted_labels[2].fields.color == "Green"

    print("PASS: Missing color handled safely.")

    # ------------------------------------------------------------
    # TEST 3: MISSING QUANTITY
    # ------------------------------------------------------------

    labels = [
        build_label("qty-2", [1], "SKU-A", 2, "Blue"),
        build_label("missing", [2], "SKU-B", None, "Red"),
        build_label("qty-1", [3], "SKU-C", 1, "Green"),
    ]

    sorted_labels = sorter.sort(
        labels,
        key="quantity",
    )

    print("\nTEST 3 - MISSING QUANTITY")

    for label in sorted_labels:
        print(
            label.id,
            "QUANTITY:",
            label.fields.quantity,
        )

    assert sorted_labels[0].fields.quantity is None
    assert sorted_labels[1].fields.quantity == 1
    assert sorted_labels[2].fields.quantity == 2

    print("PASS: Missing quantity handled safely.")

    # ------------------------------------------------------------
    # TEST 4: ORIGINAL LIST PRESERVED
    # ------------------------------------------------------------

    labels = [
        build_label("b", [1], "SKU-B", 2, "Blue"),
        build_label("missing", [2], None, 1, "Red"),
        build_label("a", [3], "SKU-A", 3, "Green"),
    ]

    original_ids = [label.id for label in labels]

    sorter.sort(
        labels,
        key="sku",
    )

    assert [label.id for label in labels] == original_ids

    print("\nTEST 4 - ORIGINAL LIST")
    print("PASS: Original list remains unchanged.")

    print("\n" + "=" * 70)
    print("ALL MISSING VALUE TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()