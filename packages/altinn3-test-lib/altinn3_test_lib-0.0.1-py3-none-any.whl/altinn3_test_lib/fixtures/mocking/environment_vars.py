import os
import pytest
from pytest_mock.plugin import MockerFixture


@pytest.fixture(scope="function")
def mock_env_wireup(mocker: MockerFixture):
    def wireup(expected_source: str = "test_app"):
        gcp_auth = mocker.patch("google.auth", autospec=True)
        gcp_auth.default.return_value = "creds", "project"
        mocker.patch.dict(
            os.environ,
            {
                "APPROVED_EVENT_SOURCE_URL": expected_source,
                "ALTINN_ARCHIVE_BUCKET": "test_bucket",
                "DB_API_BASE_URL": "base_url",
                "PROJECT_ID": "Test",
                # instantiator:
                "KEYCLOAK_SECRET_PATH": "testpath",
                "MASKINPORT_CLIENT_ID": "testclient",
                "ALTINN_PLATFORM_URL": "test_plat_url",
                "BIP_PLATFORM_ENVIRONMENT": "test_env",
                "SOURCE_BUCKET": "test_src_bucket",
                "ERROR_BUCKET": "test_err_bucket",
                "ALTINN_APP_URL": "test_app_url",
                "DB_API_URL": "test_db_url",
                "TOKEN_REFRESH_INTERVAL": "30",
            },
            clear=True,
        )

    return wireup
