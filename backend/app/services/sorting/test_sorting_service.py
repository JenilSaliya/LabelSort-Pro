from app.models.label import Label, LabelFields
from app.models.sort_options import SortOptions
from app.services.sorting.sorting_service import SortingService


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

    service = SortingService()

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

    original_ids = [label.id for label in labels]

    options = SortOptions(
        fields=[
            "courier_partner",
            "payment_type",
            "sku",
        ],
        reverse=False,
    )

    sorted_labels = service.sort_labels(
        labels,
        options,
    )

    print("=" * 70)
    print("SORTING SERVICE TEST")
    print("=" * 70)

    print("\nSORTED LABELS")

    for label in sorted_labels:
        print(
            label.id,
            label.pages,
            label.fields.courier_partner,
            label.fields.payment_type,
            label.fields.sku,
        )

    expected_ids = [
        "label-3",
        "label-1",
        "label-2",
        "label-4",
    ]

    assert [
        label.id
        for label in sorted_labels
    ] == expected_ids

    print("\nPASS: Multi-field sorting through SortingService.")

    # Original list must remain unchanged.
    assert [
        label.id
        for label in labels
    ] == original_ids

    print("PASS: Original list preserved.")

    # Multi-page labels must remain together.
    multi_page = build_label(
        "multi",
        [10, 11],
        "Valmo",
        "COD",
        "SKU-A",
    )

    labels_with_multi = [
        build_label(
            "z",
            [20],
            "Valmo",
            "COD",
            "SKU-Z",
        ),
        multi_page,
    ]

    sorted_multi = service.sort_labels(
        labels_with_multi,
        SortOptions(
            fields=["sku"],
        ),
    )

    assert sorted_multi[0].id == "multi"
    assert sorted_multi[0].pages == [10, 11]

    print("PASS: Multi-page label remained together.")

    print("\n" + "=" * 70)
    print("SORTING SERVICE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()