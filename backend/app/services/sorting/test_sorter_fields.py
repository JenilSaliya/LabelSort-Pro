from app.models.label import Label, LabelFields
from app.services.sorting.sorter import LabelSorter


def build_label(
    label_id: str,
    pages: list[int],
    *,
    courier_partner: str = "Valmo",
    payment_type: str = "COD",
    tracking_number: str = "TRACK-001",
    sku: str = "SKU-A",
    product_name: str = "Test Product",
    size: str = "6-7 Years",
    quantity: int = 1,
    color: str = "Red",
    order_number: str = "ORDER-001",
    invoice_number: str = "INV-001",
    order_date: str = "27.07.2026",
) -> Label:

    return Label(
        id=label_id,
        pages=pages,
        fields=LabelFields(
            courier_partner=courier_partner,
            payment_type=payment_type,
            tracking_number=tracking_number,
            sku=sku,
            product_name=product_name,
            size=size,
            quantity=quantity,
            color=color,
            order_number=order_number,
            invoice_number=invoice_number,
            order_date=order_date,
        ),
    )


def test_field_sorting():
    sorter = LabelSorter()

    labels = [
        build_label(
            "label-c",
            [3],
            courier_partner="Shadowfax",
            payment_type="Prepaid",
            tracking_number="TRACK-003",
            sku="SKU-C",
            product_name="Product C",
            size="8-9 Years",
            quantity=3,
            color="Yellow",
            order_number="ORDER-003",
            invoice_number="INV-003",
            order_date="29.07.2026",
        ),
        build_label(
            "label-a",
            [1],
            courier_partner="Delhivery",
            payment_type="COD",
            tracking_number="TRACK-001",
            sku="SKU-A",
            product_name="Product A",
            size="4-5 Years",
            quantity=1,
            color="Blue",
            order_number="ORDER-001",
            invoice_number="INV-001",
            order_date="27.07.2026",
        ),
        build_label(
            "label-b",
            [2],
            courier_partner="Valmo",
            payment_type="Prepaid",
            tracking_number="TRACK-002",
            sku="SKU-B",
            product_name="Product B",
            size="6-7 Years",
            quantity=2,
            color="Red",
            order_number="ORDER-002",
            invoice_number="INV-002",
            order_date="28.07.2026",
        ),
    ]

    fields = [
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
    ]

    print("=" * 70)
    print("SORTER - ALL SUPPORTED FIELDS TEST")
    print("=" * 70)

    for field in fields:

        sorted_labels = sorter.sort(
            labels,
            key=field,
        )

        values = [
            getattr(label.fields, field)
            for label in sorted_labels
        ]

        print()
        print(f"FIELD: {field}")
        print("VALUES:", values)

        expected = sorted(
            values,
            key=lambda value: (
                value.strip().lower()
                if isinstance(value, str)
                else value
            )
        )

        assert values == expected, (
            f"Sorting failed for field: {field}"
        )

        print(f"PASS: {field}")

    print()
    print("=" * 70)
    print("ALL SUPPORTED FIELD TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    test_field_sorting()