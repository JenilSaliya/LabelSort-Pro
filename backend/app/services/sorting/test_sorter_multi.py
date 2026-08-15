from app.models.label import Label, LabelFields
from app.services.sorting.sorter import LabelSorter


def build_label(
    label_id: str,
    pages: list[int],
    courier: str,
    payment: str,
    sku: str,
) -> Label:

    return Label(
        id=label_id,
        pages=pages,
        fields=LabelFields(
            courier_partner=courier,
            payment_type=payment,
            tracking_number=f"TRACK-{label_id}",
            sku=sku,
            product_name="Test Product",
            size="6-7 Years",
            quantity=1,
            color="NA",
            order_number=f"ORDER-{label_id}",
            invoice_number=f"INV-{label_id}",
            order_date="27.07.2026",
        ),
    )


def main():

    sorter = LabelSorter()

    labels = [
        build_label(
            "label-4",
            [4],
            "Valmo",
            "Prepaid",
            "SKU-B",
        ),
        build_label(
            "label-2",
            [2],
            "Valmo",
            "COD",
            "SKU-B",
        ),
        build_label(
            "label-1",
            [1],
            "Valmo",
            "COD",
            "SKU-A",
        ),
        build_label(
            "label-3",
            [3],
            "Delhivery",
            "COD",
            "SKU-A",
        ),
    ]

    print("=" * 70)
    print("MULTI-FIELD SORTER TEST")
    print("=" * 70)

    print("\nBEFORE SORTING")

    for label in labels:
        print(
            label.id,
            label.fields.courier_partner,
            label.fields.payment_type,
            label.fields.sku,
        )

    sorted_labels = sorter.sort(
        labels,
        key=[
            "courier_partner",
            "payment_type",
            "sku",
        ],
    )

    print("\nAFTER MULTI-FIELD SORTING")

    for label in sorted_labels:
        print(
            label.id,
            label.fields.courier_partner,
            label.fields.payment_type,
            label.fields.sku,
        )

    expected = [
        ("Delhivery", "COD", "SKU-A"),
        ("Valmo", "COD", "SKU-A"),
        ("Valmo", "COD", "SKU-B"),
        ("Valmo", "Prepaid", "SKU-B"),
    ]

    actual = [
        (
            label.fields.courier_partner,
            label.fields.payment_type,
            label.fields.sku,
        )
        for label in sorted_labels
    ]

    assert actual == expected, (
        f"Multi-field sorting failed.\n"
        f"Expected: {expected}\n"
        f"Actual: {actual}"
    )

    print("\nPASS: Multi-field sorting works.")

    # --------------------------------------------------------
    # ORIGINAL LIST PRESERVATION
    # --------------------------------------------------------

    original_ids = [
        label.id
        for label in labels
    ]

    assert original_ids == [
        "label-4",
        "label-2",
        "label-1",
        "label-3",
    ]

    print("PASS: Original list preserved.")

    # --------------------------------------------------------
    # MULTI-PAGE LABEL
    # --------------------------------------------------------

    multi_page = build_label(
        "multi",
        [10, 11],
        "Valmo",
        "COD",
        "SKU-A",
    )

    labels_with_multi_page = [
        build_label(
            "z",
            [20],
            "Valmo",
            "Prepaid",
            "SKU-Z",
        ),
        multi_page,
        build_label(
            "a",
            [30],
            "Delhivery",
            "COD",
            "SKU-A",
        ),
    ]

    sorted_multi = sorter.sort(
        labels_with_multi_page,
        key=[
            "courier_partner",
            "payment_type",
            "sku",
        ],
    )

    assert sorted_multi[0].id == "a"

    assert sorted_multi[1].id == "multi"

    assert sorted_multi[1].pages == [10, 11]

    assert sorted_multi[2].id == "z"

    print("PASS: Multi-page label remained together.")

    # --------------------------------------------------------
    # INVALID FIELD
    # --------------------------------------------------------

    try:
        sorter.sort(
            labels,
            key=[
                "courier_partner",
                "unknown_field",
                "sku",
            ],
        )

        raise AssertionError(
            "Unsupported multi-field did not raise ValueError"
        )

    except ValueError as exc:
        print("PASS:", exc)

    print("\n" + "=" * 70)
    print("ALL MULTI-FIELD SORTER TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()