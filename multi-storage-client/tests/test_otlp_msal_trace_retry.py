import unittest
from unittest.mock import MagicMock

from multistorageclient.telemetry.traces.exporters.otlp_msal import _OTLPMSALSpanExporter


class TestOTLPMSALSpanExporterRetry(unittest.TestCase):
    def test_retry_allows_post(self):
        mock_provider = MagicMock()
        adapter = _OTLPMSALSpanExporter.AccessTokenHTTPAdapter(
            access_token_provider=mock_provider,
            max_retries=_OTLPMSALSpanExporter._MAX_RETRIES,
        )
        self.assertIn("POST", adapter.max_retries.allowed_methods)


