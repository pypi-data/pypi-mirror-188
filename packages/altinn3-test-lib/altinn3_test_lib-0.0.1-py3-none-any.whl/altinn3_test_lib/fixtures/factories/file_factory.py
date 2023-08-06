import pytest
from ssb_altinn3_util.models.basic_file import BasicFile


@pytest.fixture(scope="function")
def basic_file_factory():
    def create_basic_file(
            filename: str,
            content_type: str = "test_content",
            b64content: str = "abcd1234test"
    ) -> BasicFile:
        return BasicFile(
            filename=filename,
            content_type=content_type,
            base64_content=b64content
        )

    return create_basic_file


@pytest.fixture(scope="function")
def create_hello():
    return "Hello!"


@pytest.fixture(scope="function")
def create_bye_bye():
    return "Bye!"
