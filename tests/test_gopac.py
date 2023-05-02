import pytest

from gopac import find_proxy


@pytest.mark.parametrize(
    'url, expected_proxy',
    [
        [
            'http://ya.ru',
            {
                'http': 'http://proxy.threatpulse.net:8080',
                'https': 'http://proxy.threatpulse.net:8080',
            },
        ],
        [
            '127.0.0.1',
            {},
        ],
    ],
)
def test_find_proxy(pac_file_path, url, expected_proxy):
    # act
    proxy = find_proxy(pac_file_path, url)

    # assert
    assert proxy == expected_proxy
