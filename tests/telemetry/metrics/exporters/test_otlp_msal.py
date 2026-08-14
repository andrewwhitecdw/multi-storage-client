# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from unittest.mock import MagicMock, patch

import pytest

from multistorageclient.telemetry.metrics.exporters.otlp_msal import (
    _OTLPMSALMetricExporter,
)


_MINIMAL_EXPORTER_CONFIG = {"endpoint": "http://localhost:4318/v1/metrics"}


@pytest.fixture
def token_provider():
    with patch(
        "multistorageclient.telemetry.metrics.exporters.otlp_msal.AzureAccessTokenProvider"
    ) as mocked:
        mocked.return_value = MagicMock()
        yield mocked


@pytest.fixture
def no_keep_alive_env():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("MSC_OTEL_EXPORTER_KEEP_ALIVE", None)
        yield


def test_connection_close_when_keep_alive_unset(no_keep_alive_env, token_provider):
    exporter = _OTLPMSALMetricExporter(
        auth={"client_id": "test"}, exporter=_MINIMAL_EXPORTER_CONFIG
    )
    assert exporter._session.headers.get("Connection") == "close"


def test_connection_close_when_keep_alive_empty(no_keep_alive_env, token_provider):
    with patch.dict(os.environ, {"MSC_OTEL_EXPORTER_KEEP_ALIVE": ""}):
        exporter = _OTLPMSALMetricExporter(
            auth={"client_id": "test"}, exporter=_MINIMAL_EXPORTER_CONFIG
        )
        assert exporter._session.headers.get("Connection") == "close"


def test_connection_header_absent_when_keep_alive_enabled(no_keep_alive_env, token_provider):
    with patch.dict(os.environ, {"MSC_OTEL_EXPORTER_KEEP_ALIVE": "1"}):
        exporter = _OTLPMSALMetricExporter(
            auth={"client_id": "test"}, exporter=_MINIMAL_EXPORTER_CONFIG
        )
        assert "Connection" not in exporter._session.headers
