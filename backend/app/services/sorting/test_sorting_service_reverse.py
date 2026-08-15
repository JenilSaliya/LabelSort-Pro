from app.models.label import Label, LabelFields
from app.models.sort_options import SortOptions
from app.services.sorting.sorting_service import SortingService


def build_label(
    label_id: str,
    pages: list[int],
    sku: str,
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
        build_label("label-a", [1], "SKU-A"),
        build_label("label-c", [3], "SKU-C"),
        build_label("label-b", [2], "SKU-B"),
    ]

    original_ids = [label.id for label in labels]

    options = SortOptions(
        fields=["sku"],
        reverse=True,
    )

    sorted_labels = service.sort_labels(
        labels,
        options,
    )

    print("=" * 70)
    print("SORTING SERVICE - REVERSE TEST")
    print("=" * 70)

    print("\nREVERSE SORTING")

    for label in sorted_labels:
        print(
            label.id,
            label.pages,
            label.fields.sku,
        )

    expected_ids = [
        "label-c",
        "label-b",
        "label-a",
    ]

    assert [
        label.id
        for label in sorted_labels
    ] == expected_ids

    print("\nPASS: Reverse sorting through SortingService.")

    assert [
        label.id
        for label in labels
    ] == original_ids

    print("PASS: Original list preserved.")

    print("\n" + "=" * 70)
    print("REVERSE SORTING SERVICE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()