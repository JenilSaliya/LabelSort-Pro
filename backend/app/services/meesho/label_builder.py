from app.models.label import Label, LabelFields


def build_label(parsed: dict) -> Label:
    """
    Convert one parser result into the application's Label model.
    """

    fields = LabelFields(
        courier_partner=parsed.get("courier_partner"),
        payment_type=parsed.get("payment_type"),
        tracking_number=parsed.get("tracking_number"),
        sku=parsed.get("sku"),
        product_name=parsed.get("product_name"),
        size=parsed.get("size"),
        quantity=parsed.get("quantity"),
        color=parsed.get("color"),
        order_number=parsed.get("order_number"),
        invoice_number=parsed.get("invoice_number"),
        order_date=parsed.get("order_date"),
    )

    page_number = parsed["page_number"]

    return Label(
        id=f"page-{page_number}",
        pages=[page_number],
        fields=fields,
    )