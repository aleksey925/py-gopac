from pathlib import Path

import pytest

from gopac import download_pac_file, find_proxy, terminate_download_pac_file
from gopac.gopac import get_terminate_download_flag


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


def test_download_pac_file(mocker):
    # arrange
    urlretrieve_mock = mocker.patch('gopac.gopac.urlretrieve')
    url = 'http://example.com/pacfile.pac'
    path = Path('./file.pac')
    terminate_download_pac_file()
    terminate_download_flag_before = get_terminate_download_flag()

    # act
    path_to_file = download_pac_file(url, path=path)

    # assert
    urlretrieve_mock.assert_called_once_with(url, path, reporthook=mocker.ANY)
    assert path_to_file == path
    assert terminate_download_flag_before is True
    assert get_terminate_download_flag() is False


def test_download_pac_file__download_to_temp_dir__success(mocker):
    # arrange
    url = 'http://example.com/pacfile.pac'
    expected_base_path = '/tmp/34b3v'
    expected_filename = 'aHR0cDovL2V4YW1wbGUuY29tL3BhY2ZpbGUucGFj.pac'
    expected_path_to_file = Path(expected_base_path) / Path(expected_filename)
    mocker.patch('gopac.gopac.gettempdir', return_value=expected_base_path)
    urlretrieve_mock = mocker.patch('gopac.gopac.urlretrieve')

    # act
    path_to_file = download_pac_file(url)

    # assert
    urlretrieve_mock.assert_called_once_with(url, expected_path_to_file, reporthook=mocker.ANY)
    assert path_to_file == expected_path_to_file
