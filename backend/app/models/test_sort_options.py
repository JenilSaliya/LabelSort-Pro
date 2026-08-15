from app.models.sort_options import SortOptions


def main():

    print("=" * 70)
    print("SORT OPTIONS MODEL TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # TEST 1 - SINGLE FIELD
    # --------------------------------------------------------

    options = SortOptions(
        fields=["sku"]
    )

    print("\nTEST 1 - SINGLE FIELD")

    print("fields:", options.fields)
    print("reverse:", options.reverse)

    assert options.fields == ["sku"]
    assert options.reverse is False

    print("PASS: Single-field options.")

    # --------------------------------------------------------
    # TEST 2 - MULTIPLE FIELDS
    # --------------------------------------------------------

    options = SortOptions(
        fields=[
            "courier_partner",
            "payment_type",
            "sku",
        ]
    )

    print("\nTEST 2 - MULTIPLE FIELDS")

    print("fields:", options.fields)
    print("reverse:", options.reverse)

    assert options.fields == [
        "courier_partner",
        "payment_type",
        "sku",
    ]

    print("PASS: Multi-field options.")

    # --------------------------------------------------------
    # TEST 3 - REVERSE
    # --------------------------------------------------------

    options = SortOptions(
        fields=["sku"],
        reverse=True,
    )

    print("\nTEST 3 - REVERSE")

    print("fields:", options.fields)
    print("reverse:", options.reverse)

    assert options.reverse is True

    print("PASS: Reverse option.")

    # --------------------------------------------------------
    # TEST 4 - EMPTY FIELDS
    # --------------------------------------------------------

    print("\nTEST 4 - EMPTY FIELDS")

    try:
        SortOptions(fields=[])

        raise AssertionError(
            "Empty fields should not be accepted"
        )

    except Exception as exc:
        print("PASS: Empty fields rejected.")
        print(type(exc).__name__)

    print("\n" + "=" * 70)
    print("ALL SORT OPTIONS TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()