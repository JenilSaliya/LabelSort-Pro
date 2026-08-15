from app.models.label import Label, LabelFields
from app.services.sorting.sorter import LabelSorter


def build_label(
    label_id: str,
    pages: list[int],
    sku: str | None,
    quantity: int | None = 1,
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
            color="NA",
            order_number=f"ORDER-{label_id}",
            invoice_number=f"INV-{label_id}",
            order_date="27.07.2026",
        ),
    )


def main():

    sorter = LabelSorter()

    print("=" * 70)
    print("LABEL SORTER - COMPLETE TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # TEST 1: ASCENDING SKU
    # ------------------------------------------------------------

    labels = [
        build_label("label-c", [1], "SKU-C"),
        build_label("label-a", [2], "SKU-A"),
        build_label("label-b", [3], "SKU-B"),
    ]

    original_ids = [label.id for label in labels]

    sorted_labels = sorter.sort(
        labels,
        key="sku",
    )

    print("\nTEST 1 - ASCENDING SKU")

    for label in sorted_labels:
        print(
            label.id,
            label.pages,
            label.fields.sku,
        )

    assert [label.fields.sku for label in sorted_labels] == [
        "SKU-A",
        "SKU-B",
        "SKU-C",
    ], "SKU ascending sort failed"

    print("PASS: Ascending SKU sorting works.")

    # Original list must remain unchanged.
    assert [
        label.id
        for label in labels
    ] == original_ids

    print("PASS: Ascending SKU sorting.")
    print("PASS: Original list preserved.")

    # ------------------------------------------------------------
    # TEST 2: DESCENDING SKU
    # ------------------------------------------------------------

    descending = sorter.sort(
        labels,
        key="sku",
        reverse=True,
    )

    print("\nTEST 2 - DESCENDING SKU")

    for label in descending:
        print(
            label.id,
            label.pages,
            label.fields.sku,
        )

    assert [label.id for label in descending] == [
        "label-c",
        "label-b",
        "label-a",
    ], "Descending SKU sorting order is incorrect."

    print("PASS: Descending SKU sorting works.")

    print("PASS: Descending SKU sorting.")

    # ------------------------------------------------------------
    # TEST 3: MULTI-PAGE LABEL
    # ------------------------------------------------------------

    multi_page = build_label(
        "multi",
        [10, 11],
        "SKU-A",
    )

    multi_labels = [
        build_label("z", [20], "SKU-Z"),
        multi_page,
        build_label("b", [30], "SKU-B"),
    ]

    sorted_multi = sorter.sort(
        multi_labels,
        key="sku",
    )

    print("\nTEST 3 - MULTI-PAGE LABEL")

    for label in sorted_multi:
        print(
            label.id,
            label.pages,
            label.fields.sku,
        )

    assert sorted_multi[0].id == "multi"
    assert sorted_multi[0].pages == [10, 11]

    print("PASS: Multi-page label remained together.")

    # ------------------------------------------------------------
    # TEST 4: MISSING SKU
    # ------------------------------------------------------------

    missing_labels = [
        build_label("sku-b", [1], "SKU-B"),
        build_label("missing", [2], None),
        build_label("sku-a", [3], "SKU-A"),
    ]

    sorted_missing = sorter.sort(
        missing_labels,
        key="sku",
    )

    print("\nTEST 4 - MISSING SKU")

    for label in sorted_missing:
        print(
            label.id,
            label.pages,
            label.fields.sku,
        )

    assert sorted_missing[0].fields.sku is None
    assert sorted_missing[1].fields.sku == "SKU-A"
    assert sorted_missing[2].fields.sku == "SKU-B"

    print("PASS: Missing SKU handled safely.")

    # ------------------------------------------------------------
    # TEST 5: QUANTITY SORTING
    # ------------------------------------------------------------

    quantity_labels = [
        build_label("qty-3", [1], "SKU-A", 3),
        build_label("qty-1", [2], "SKU-B", 1),
        build_label("qty-2", [3], "SKU-C", 2),
    ]

    sorted_quantity = sorter.sort(
        quantity_labels,
        key="quantity",
    )

    print("\nTEST 5 - QUANTITY")

    for label in sorted_quantity:
        print(
            label.id,
            label.fields.quantity,
        )

    assert [
        label.fields.quantity
        for label in sorted_quantity
    ] == [1, 2, 3]

    print("PASS: Numeric quantity sorting.")

    # ------------------------------------------------------------
    # TEST 6: UNSUPPORTED FIELD
    # ------------------------------------------------------------

    print("\nTEST 6 - INVALID SORT FIELD")

    try:
        sorter.sort(
            labels,
            key="unknown_field",
        )

        raise AssertionError(
            "Unsupported field did not raise ValueError"
        )

    except ValueError as exc:
        print("PASS:", exc)

    # ------------------------------------------------------------
    # FINAL
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("ALL SORTER TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()