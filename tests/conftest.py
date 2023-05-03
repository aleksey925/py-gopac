from pathlib import Path

import pytest

test_base_dir = Path(__file__).absolute().parent


@pytest.fixture
def pac_file_path():
    return test_base_dir / 'data' / 'proxy.pac'
