from app.models.label import Label, LabelFields


fields = LabelFields(
    courier_partner="ValmoPlus",
    payment_type="COD",
    tracking_number="VL0084940276858",
    sku="3 D TEDDY & PLAN WHITE P",
    product_name="Kid Clothing,kids combo set,kids co ord set - 6-7 Years",
    size="6-7 Years",
    quantity=1,
    color="NA",
    order_number="313354414974188736",
    invoice_number="he1mq27471",
    order_date="27.07.2026",
)


label = Label(
    id="label-001",
    pages=[1],
    fields=fields,
)


print("\n========== LABEL MODEL ==========\n")
print(label)
print("\n========== AS DICT ==========\n")
print(label.model_dump())