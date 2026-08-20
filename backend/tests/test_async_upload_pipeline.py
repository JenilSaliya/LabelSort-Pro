import io
from fastapi.testclient import TestClient
import pymupdf as fitz
from pathlib import Path
from datetime import datetime, timedelta

from app.main import app
from app.services.job.job_service import JobService
from app.services.processing.upload_processor import UploadProcessor
from app.services.meesho.parser import MeeshoParser
from app.services.cleanup.cleanup_service import CleanupService
from app.core.constants import (
    STATUS_QUEUED,
    STATUS_PROCESSING,
    STATUS_COMPLETED,
    STATUS_FAILED,
)

client = TestClient(app)


def create_sample_meesho_pdf_bytes(num_pages: int = 3) -> bytes:
    """Helper to generate a valid in-memory Meesho PDF test fixture."""
    doc = fitz.open()
    sample_text = (
        "Meesho\n"
        "Return/Selling\n"
        "Courier: Delhivery Surface\n"
        "Tracking No: 140123456789012\n"
        "Product Details\n"
        "SKU Size Qty Color Order No.\n"
        "KURTI-BLUE XL 1 Blue 313354414974188736_1\n"
        "TAX INVOICE\n"
        "Description HSN Qty Gross Amount Discount Taxable Value Taxes Total\n"
        "Women Rayon Kurti 6104 1 Rs. 499 0 Rs. 475 Rs. 24 Rs. 499\n"
        "Purchase Order No. PO-998811\n"
        "Invoice No. INV-100234\n"
        "Order Date 18.08.2026\n"
        "Payment: COD\n"
    )
    for i in range(num_pages):
        page = doc.new_page()
        page.insert_text((50, 50), f"Page {i+1}\n" + sample_text)

    buf = io.BytesIO()
    doc.save(buf)
    doc.close()
    return buf.getvalue()


# ------------------------------------------------------------
# 1. TEST UPLOAD ENDPOINT (FAST ASYNC RETURN)
# ------------------------------------------------------------
def test_upload_endpoint_returns_immediately_with_job_id():
    pdf_bytes = create_sample_meesho_pdf_bytes(2)
    files = [("files", ("test_labels.pdf", pdf_bytes, "application/pdf"))]

    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "job_id" in data["data"]
    assert data["data"]["status"] == STATUS_QUEUED
    assert data["data"]["uploaded_file_count"] == 1


def test_upload_endpoint_rejects_non_pdf():
    files = [("files", ("test.txt", b"Hello world", "text/plain"))]
    response = client.post("/upload/", files=files)
    assert response.status_code == 400


def test_upload_endpoint_rejects_empty_file():
    files = [("files", ("empty.pdf", b"", "application/pdf"))]
    response = client.post("/upload/", files=files)
    assert response.status_code == 400


# ------------------------------------------------------------
# 2. TEST UPLOAD PROCESSOR & PROGRESS TRACKING
# ------------------------------------------------------------
def test_upload_processor_full_lifecycle():
    job_service = JobService()
    job = job_service.create_job()
    job_id = job["job_id"]
    job_dir = job["job_dir"]

    # Place original PDF
    pdf_bytes = create_sample_meesho_pdf_bytes(4)
    original_path = job_dir / "original" / "original.pdf"
    with open(original_path, "wb") as f:
        f.write(pdf_bytes)

    processor = UploadProcessor()
    processor.process_upload_job(job_id)

    # Verify completed metadata
    metadata = job_service.get_job(job_id)
    assert metadata["status"] == STATUS_COMPLETED
    assert metadata["progress"] == 100
    assert metadata["current_step"] == "completed"
    assert metadata["page_count"] == 4
    assert metadata["label_groups"] == 4
    assert metadata["marketplace"] == "meesho"

    # Verify cached labels exist
    labels_path = job_dir / "extracted" / "labels.json"
    assert labels_path.exists()

    # Verify reports exist
    analysis_path = job_dir / "reports" / "analysis.json"
    excel_path = job_dir / "reports" / "statistics.xlsx"
    assert analysis_path.exists()
    assert excel_path.exists()


# ------------------------------------------------------------
# 3. TEST JOB FAILURE HANDLING (PRESERVES JOB RECORD)
# ------------------------------------------------------------
def test_upload_processor_failure_handling():
    job_service = JobService()
    job = job_service.create_job()
    job_id = job["job_id"]
    job_dir = job["job_dir"]

    # Place a corrupt PDF file
    original_path = job_dir / "original" / "original.pdf"
    with open(original_path, "wb") as f:
        f.write(b"%PDF-1.4 corrupt junk bytes that cannot be parsed")

    processor = UploadProcessor()
    processor.process_upload_job(job_id)

    # Job should NOT be deleted, but marked as failed with error details
    metadata = job_service.get_job(job_id)
    assert metadata["status"] == STATUS_FAILED
    assert metadata["current_step"] == "failed"
    assert metadata["error"] is not None
    assert len(metadata["error"]) > 0


# ------------------------------------------------------------
# 4. TEST MEESHO PARSER CORRECTNESS & SPEED
# ------------------------------------------------------------
def test_meesho_parser_extracted_fields():
    parser = MeeshoParser()
    sample_text = (
        "Meesho Return Label\n"
        "ValmoPlus Delivery\n"
        "Tracking: VL0084940276858\n"
        "Product Details\n"
        "SKU Size Qty Color Order No.\n"
        "BLUE-KURTI 2-3 Years 2 Navy 987654321012_1\n"
        "TAX INVOICE\n"
        "Description HSN Qty Gross Amount Discount Taxable Value Taxes Total\n"
        "Navy Cotton Kurti 610400 2 Rs. 899 0 Rs. 850 Rs. 49 Rs. 899\n"
        "Purchase Order No. PO-445566\n"
        "Invoice No. INV-998877\n"
        "Order Date 19.08.2026\n"
        "Prepaid\n"
    )

    res = parser.parse_page(sample_text, 1)
    assert res["page_number"] == 1
    assert res["courier_partner"] == "ValmoPlus"
    assert res["payment_type"] == "Prepaid"
    assert res["tracking_number"] == "VL0084940276858"
    assert res["sku"] == "BLUE-KURTI"
    assert res["size"] == "2-3 Years"
    assert res["quantity"] == 2
    assert res["color"] == "Navy"
    assert res["order_number"] == "PO-445566"
    assert res["invoice_number"] == "INV-998877"
    assert res["order_date"] == "19.08.2026"
    assert res["product_name"] == "Navy Cotton Kurti"


# ------------------------------------------------------------
# 5. TEST CLEANUP SERVICE PROTECTS ACTIVE IN-FLIGHT JOBS
# ------------------------------------------------------------
def test_cleanup_service_protects_active_jobs():
    job_service = JobService()
    cleanup = CleanupService()

    # Create active in-flight job (10 minutes old)
    job = job_service.create_job()
    job_id = job["job_id"]
    job_dir = job["job_dir"]

    metadata = job_service.get_job(job_id)
    metadata["status"] = STATUS_PROCESSING
    metadata["updated_at"] = (datetime.now() - timedelta(minutes=10)).isoformat()
    job_service.save_metadata(job_id, metadata)

    # Run cleanup
    cleanup.cleanup_old_jobs()

    # Active job MUST STILL EXIST!
    assert job_dir.exists()

    # Clean up test workspace
    job_service.delete_job(job_id)
