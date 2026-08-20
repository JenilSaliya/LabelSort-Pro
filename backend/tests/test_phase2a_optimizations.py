import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.job import JobMetadata
from app.services.meesho.parser import MeeshoParser
from app.services.extraction.extraction_service import ExtractionService
from app.services.processing.upload_processor import UploadProcessor
from app.services.job.job_service import JobService
from app.core.constants import STATUS_COMPLETED


class Phase2AOptimizationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.parser = MeeshoParser()
        self.job_service = JobService()

    def test_job_metadata_telemetry_schema(self):
        """Verify all new Phase 2A telemetry fields are present in JobMetadata schema."""
        meta = JobMetadata(
            job_id="test_job_123",
            status="processing",
            progress=45,
            current_step="extracting",
            status_message="Extracting page 45 of 100...",
            pages_processed=45,
            total_pages=100,
            elapsed_seconds=3.2,
            eta_seconds=4,
            eta_formatted="~4s remaining",
            processing_speed_pps=14.1,
        )
        dumped = meta.model_dump()
        self.assertEqual(dumped["progress"], 45)
        self.assertEqual(dumped["current_step"], "extracting")
        self.assertEqual(dumped["status_message"], "Extracting page 45 of 100...")
        self.assertEqual(dumped["pages_processed"], 45)
        self.assertEqual(dumped["total_pages"], 100)
        self.assertEqual(dumped["elapsed_seconds"], 3.2)
        self.assertEqual(dumped["eta_seconds"], 4)
        self.assertEqual(dumped["eta_formatted"], "~4s remaining")
        self.assertEqual(dumped["processing_speed_pps"], 14.1)

    def test_parser_invoice_short_circuit(self):
        """Verify invoice short-circuit logic works accurately on full vs cropped labels."""
        full_text = (
            "Meesho Shipping Label\n"
            "Valmo Pickup\n"
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
        )
        cropped_text = (
            "Exchange\n"
            "Shadowfax Pickup\n"
            "SF3807144630MEO\n"
            "Product Details\n"
            "SKU Size Qty Color Order No.\n"
            "TOP-SET-BLUE 3-4 Years 1 Navy 313326578632696576_1\n"
        )

        full_res = self.parser.parse_page(full_text, 1)
        self.assertEqual(full_res["sku"], "TOP-SET-BLUE")
        self.assertEqual(full_res["invoice_number"], "INV-554433")
        self.assertEqual(full_res["order_number"], "PO-889900")
        self.assertEqual(full_res["product_name"], "Modern Boys Top Set")

        cropped_res = self.parser.parse_page(cropped_text, 2)
        self.assertEqual(cropped_res["sku"], "TOP-SET-BLUE")
        self.assertIsNone(cropped_res["invoice_number"])
        self.assertIsNone(cropped_res["order_number"])
        self.assertIsNone(cropped_res["product_name"])

    def test_health_check_triggers_background_cleanup(self):
        """Verify GET and HEAD /health/ respond 200 OK and invoke cleanup."""
        resp_get = self.client.get("/health/")
        self.assertEqual(resp_get.status_code, 200)
        self.assertEqual(resp_get.json()["status"], "ok")

        resp_head = self.client.head("/health/")
        self.assertEqual(resp_head.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
