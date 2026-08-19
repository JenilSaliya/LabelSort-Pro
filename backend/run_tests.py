import sys
import unittest
from pathlib import Path

# Add backend to PYTHONPATH
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from tests.test_async_upload_pipeline import (
    test_upload_endpoint_returns_immediately_with_job_id,
    test_upload_endpoint_rejects_non_pdf,
    test_upload_endpoint_rejects_empty_file,
    test_upload_processor_full_lifecycle,
    test_upload_processor_failure_handling,
    test_meesho_parser_extracted_fields,
    test_cleanup_service_protects_active_jobs,
)

class AsyncUploadPipelineTests(unittest.TestCase):
    def test_upload_endpoint_fast_return(self):
        test_upload_endpoint_returns_immediately_with_job_id()

    def test_upload_endpoint_rejects_non_pdf(self):
        test_upload_endpoint_rejects_non_pdf()

    def test_upload_endpoint_rejects_empty_file(self):
        test_upload_endpoint_rejects_empty_file()

    def test_upload_processor_full_lifecycle(self):
        test_upload_processor_full_lifecycle()

    def test_upload_processor_failure_handling(self):
        test_upload_processor_failure_handling()

    def test_meesho_parser_extracted_fields(self):
        test_meesho_parser_extracted_fields()

    def test_cleanup_service_protects_active_jobs(self):
        test_cleanup_service_protects_active_jobs()

if __name__ == "__main__":
    unittest.main(verbosity=2)
