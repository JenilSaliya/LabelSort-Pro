from app.models.label import Label, LabelFields
from app.services.output.page_order import PageOrderBuilder


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

    print("=" * 70)
    print("PAGE ORDER BUILDER TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # TEST 1 - SINGLE PAGE LABELS
    # ---------------------------------------------------------

    labels = [
        build_label("A", [2], "SKU-A"),
        build_label("B", [5], "SKU-B"),
        build_label("C", [1], "SKU-C"),
    ]

    page_order = PageOrderBuilder.build(labels)

    print("\nTEST 1 - SINGLE PAGE LABELS")
    print("PAGE ORDER:", page_order)

    assert page_order == [2, 5, 1]

    print("PASS: Single-page order generated.")

    # ---------------------------------------------------------
    # TEST 2 - MULTI-PAGE LABEL
    # ---------------------------------------------------------

    labels = [
        build_label("A", [10, 11], "SKU-A"),
        build_label("B", [2], "SKU-B"),
        build_label("C", [7, 8], "SKU-C"),
    ]

    page_order = PageOrderBuilder.build(labels)

    print("\nTEST 2 - MULTI-PAGE LABEL")
    print("PAGE ORDER:", page_order)

    assert page_order == [10, 11, 2, 7, 8]

    print("PASS: Multi-page labels remain together.")

    # ---------------------------------------------------------
    # TEST 3 - EMPTY LIST
    # ---------------------------------------------------------

    page_order = PageOrderBuilder.build([])

    print("\nTEST 3 - EMPTY LABEL LIST")
    print("PAGE ORDER:", page_order)

    assert page_order == []

    print("PASS: Empty label list handled safely.")

    # ---------------------------------------------------------
    # FINAL
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("ALL PAGE ORDER TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()