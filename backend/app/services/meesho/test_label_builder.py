from app.services.meesho.label_builder import build_label


def main():
    parsed = {
        "page_number": 1,
        "courier_partner": "ValmoPlus",
        "payment_type": "COD",
        "tracking_number": "VL0084940276858",
        "sku": "3 D TEDDY & PLAN WHITE P",
        "product_name": (
            "Kid Clothing,kids combo set,"
            "kids co ord set - 6-7 Years"
        ),
        "size": "6-7 Years",
        "quantity": 1,
        "color": "NA",
        "order_number": "313354414974188736",
        "invoice_number": "he1mq27471",
        "order_date": "27.07.2026",
    }

    label = build_label(parsed)

    print("=" * 70)
    print("LABEL MODEL TEST")
    print("=" * 70)

    print("id              :", label.id)
    print("pages           :", label.pages)
    print("courier_partner :", label.fields.courier_partner)
    print("payment_type    :", label.fields.payment_type)
    print("tracking_number :", label.fields.tracking_number)
    print("sku             :", label.fields.sku)
    print("product_name    :", label.fields.product_name)
    print("size            :", label.fields.size)
    print("quantity        :", label.fields.quantity)
    print("color           :", label.fields.color)
    print("order_number    :", label.fields.order_number)
    print("invoice_number  :", label.fields.invoice_number)
    print("order_date      :", label.fields.order_date)

    assert label.id == "page-1"
    assert label.pages == [1]

    assert label.fields.courier_partner == "ValmoPlus"
    assert label.fields.payment_type == "COD"
    assert label.fields.tracking_number == "VL0084940276858"
    assert label.fields.sku == "3 D TEDDY & PLAN WHITE P"
    assert label.fields.size == "6-7 Years"
    assert label.fields.quantity == 1
    assert label.fields.color == "NA"
    assert label.fields.order_number == "313354414974188736"
    assert label.fields.invoice_number == "he1mq27471"
    assert label.fields.order_date == "27.07.2026"

    print()
    print("=" * 70)
    print("LABEL MODEL TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()