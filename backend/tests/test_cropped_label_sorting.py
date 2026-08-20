import unittest
from app.services.marketplace.detector import MarketplaceDetector, Marketplace
from app.services.meesho.parser import MeeshoParser
from app.services.meesho.label_builder import build_label
from app.services.sorting.sorter import LabelSorter


class CroppedLabelSortingTests(unittest.TestCase):
    def setUp(self):
        self.detector = MarketplaceDetector()
        self.parser = MeeshoParser()
        self.sorter = LabelSorter()

    def test_marketplace_detection_on_cropped_page(self):
        """Verify Meesho is detected even when first page is a cropped label."""
        cropped_shadowfax = (
            "Customer Address\n"
            "If undelivered, return to:\n"
            "Exchange\n"
            "Shadowfax\n"
            "Pickup\n"
            "Destination Code\n"
            "N17_PBH\n"
            "_Mand\n"
            "Return Code\n"
            "394107,2719985\n"
            "SF3807144630MEO\n"
            "Product Details\n"
            "SKU Size Qty Color Order No.\n"
            "3D TEDDY END PLANE WHITE 3-4 Years 1 NA 317540220366803904_1\n"
        )
        self.assertEqual(self.detector.detect(cropped_shadowfax), Marketplace.MEESHO)

    def test_full_label_extraction(self):
        """Verify standard full Meesho label with TAX INVOICE extracts all fields."""
        full_text = (
            "Meesho Shipping Label\n"
            "ValmoPlus Pickup\n"
            "VL0084940645781\n"
            "Product Details\n"
            "SKU Size Qty Color Order No.\n"
            "TOP-SET-BLUE 3-4 Years 1 Navy 313326578632696576_1\n"
            "TAX INVOICE\n"
            "Description HSN Qty Gross Amount Discount Taxable Value Taxes Total\n"
            "Modern Boys Top Set 610400 1 Rs. 299 0 Rs. 280 Rs. 19 Rs. 299\n"
            "Purchase Order No. PO-889900\n"
            "Invoice No. INV-554433\n"
            "Order Date 20.08.2026\n"
            "Payment: COD\n"
        )
        res = self.parser.parse_page(full_text, 1)
        self.assertEqual(res["courier_partner"], "ValmoPlus")
        self.assertEqual(res["tracking_number"], "VL0084940645781")
        self.assertEqual(res["sku"], "TOP-SET-BLUE")
        self.assertEqual(res["size"], "3-4 Years")
        self.assertEqual(res["quantity"], 1)
        self.assertEqual(res["color"], "Navy")
        self.assertEqual(res["order_number"], "PO-889900")
        self.assertEqual(res["invoice_number"], "INV-554433")
        self.assertEqual(res["order_date"], "20.08.2026")
        self.assertEqual(res["product_name"], "Modern Boys Top Set")

    def test_user_6page_pdf_extraction_and_sorting(self):
        """
        Exact test with the 6 pages provided by user:
        - Pages 1-4: Cropped Shadowfax labels (Sizes: 3-4 Years, 4-5 Years)
        - Pages 5-6: Full Valmo labels (Size: 0-1 Years)
        """
        pages = [
            # Page 1: Cropped Shadowfax
            ("Customer Address\nIf undelivered, return to:\nExchange\nShadowfax\nPickup\n"
             "Destination Code\nN17_PBH\n_Mand\nReturn Code\n394107,2719985\nSF3807144630MEO\n"
             "Product Details\nSKU Size Qty Color Order No.\n"
             "3D TEDDY END PLANE WHITE 3-4 Years 1 NA 317540220366803904_1", 1),
            # Page 2: Cropped Shadowfax
            ("Customer Address\nIf undelivered, return to:\nExchange\nShadowfax\nPickup\n"
             "Destination Code\nW20_BOM\n_Kara\nReturn Code\n394107,2719985\nSF3811300443MEO\n"
             "Product Details\nSKU Size Qty Color Order No.\n"
             "3D TEDDY END PLANE WHITE 4-5 Years 1 NA 319124681554412352_1", 2),
            # Page 3: Cropped Shadowfax
            ("Customer Address\nIf undelivered, return to:\nExchange\nShadowfax\nPickup\n"
             "Destination Code\nN13_NYO\n_Naya\nReturn Code\n394107,2719985\nSF3807160318MEO\n"
             "Product Details\nSKU Size Qty Color Order No.\n"
             "3D TEDDY END PLANE WHITE 4-5 Years 1 NA 318472008231183744_1", 3),
            # Page 4: Cropped Shadowfax
            ("Customer Address\nIf undelivered, return to:\nExchange\nShadowfax\nPickup\n"
             "Destination Code\nN9_AGR_\nArju\nReturn Code\n394107,2719985\nSF3822481539MEO\n"
             "Product Details\nSKU Size Qty Color Order No.\n"
             "3D TEDDY END PLANE WHITE 3-4 Years 1 NA 318960186268694336_1", 4),
            # Page 5: Full Valmo
            ("Customer Address\nIf undelivered, return to:\nCheck the payable amount on the app\n"
             "Valmo Pickup 26/08\nWA8-R0\nW1/SCS\nE1/MZPS\n8/MZF\nVL0085137072904\n"
             "Product Details\nSKU Size Qty Color Order No.\n"
             "3D TEDDY END PLANE WHITE 0-1 Years 1 NA 320533355760610880_1\n"
             "TAX INVOICE Original For Recipient\nBILL TO / SHIP TO\nPurchase Order No.\n"
             "320533355760610880\nInvoice No.\nyh7592769948\nOrder Date\n16.08.2026\n"
             "Description HSN Qty Gross Amount Discount Taxable Value Taxes Total\n"
             "Cutiepie Boys Set 62092000 1 Rs.186.99 Rs.0.00 Rs.178.09 IGST @5.0% Rs.8.90 Rs.186.99", 5),
            # Page 6: Full Valmo
            ("Customer Address\nIf undelivered, return to:\nCheck the payable amount on the app\n"
             "Valmo Pickup 28/08\nWA8-R0\nW1/SCS\nN1/LDNS\nPB7/FRD\nVL0085137072897\n"
             "Product Details\nSKU Size Qty Color Order No.\n"
             "3D TEDDY END PLANE WHITE 0-1 Years 1 NA 320455217005573440_1\n"
             "TAX INVOICE Original For Recipient\nBILL TO / SHIP TO\nPurchase Order No.\n"
             "320455217005573440\nInvoice No.\nyh7592769889\nOrder Date\n16.08.2026\n"
             "Description HSN Qty Gross Amount Discount Taxable Value Taxes Total\n"
             "Cutiepie Boys Set 62092000 1 Rs.183.99 Rs.0.00 Rs.175.23 IGST @5.0% Rs.8.76 Rs.183.99", 6),
        ]

        labels = []
        for text, pg_num in pages:
            parsed = self.parser.parse_page(text, pg_num)
            label = build_label(parsed)
            labels.append(label)

        # Verify all 6 pages have exact SKU and Size extracted
        for l in labels:
            self.assertEqual(l.fields.sku, "3D TEDDY END PLANE WHITE")
            self.assertIsNotNone(l.fields.size)
            self.assertIsNotNone(l.fields.courier_partner)

        # 1. Sort with Valmo prioritized over Shadowfax
        sorted_valmo_first = self.sorter.sort_multiple(
            labels=labels,
            keys=["courier_partner", "sku", "size"],
            courier_priority=["Valmo", "Shadowfax"],
        )

        # Valmo pages (5, 6) must come first!
        self.assertEqual(sorted_valmo_first[0].fields.courier_partner, "Valmo")
        self.assertEqual(sorted_valmo_first[1].fields.courier_partner, "Valmo")
        self.assertEqual(sorted_valmo_first[2].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_valmo_first[3].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_valmo_first[4].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_valmo_first[5].fields.courier_partner, "Shadowfax")

        # Within Shadowfax, sizes should be 3-4 Years (pg 1, 4) then 4-5 Years (pg 2, 3)
        shadowfax_sizes = [l.fields.size for l in sorted_valmo_first[2:]]
        self.assertEqual(shadowfax_sizes, ["3-4 Years", "3-4 Years", "4-5 Years", "4-5 Years"])

        # 2. Sort with Shadowfax prioritized over Valmo
        sorted_shadowfax_first = self.sorter.sort_multiple(
            labels=labels,
            keys=["courier_partner", "sku", "size"],
            courier_priority=["Shadowfax", "Valmo"],
        )
        self.assertEqual(sorted_shadowfax_first[0].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_shadowfax_first[1].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_shadowfax_first[2].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_shadowfax_first[3].fields.courier_partner, "Shadowfax")
        self.assertEqual(sorted_shadowfax_first[4].fields.courier_partner, "Valmo")
        self.assertEqual(sorted_shadowfax_first[5].fields.courier_partner, "Valmo")


if __name__ == "__main__":
    unittest.main(verbosity=2)
