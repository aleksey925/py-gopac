import base64
import ctypes
import json
import logging
from pathlib import Path
from tempfile import gettempdir

import requests

from gopac.exceptions import SharedLibraryNotFound, DownloadCancel, GoPacException

__all__ = ['find_proxy', 'download_pac_file', 'terminate_download_pac_file']

from gopac.structures import GoStr

logger = logging.getLogger()
extension_dir = Path(__file__).parent.absolute() / 'extension'
_downloader_state = {'terminate_download': False}


def find_shared_library() -> Path:
    shared_library = list(filter(
        lambda i: not i.name.endswith('.py') and i.name != '__pycache__', extension_dir.iterdir()
    ))
    if len(shared_library) != 1:
        raise SharedLibraryNotFound()
    return shared_library[0]


lib = ctypes.cdll.LoadLibrary(str(find_shared_library()))
lib.ParseFile.argtypes = [GoStr, GoStr]
lib.ParseFile.restype = ctypes.c_char_p


def get_pac_path(url):
    return Path(gettempdir()) / f'{base64.b64encode(url.encode()).decode()}.pac'


def download_pac_file(url: str, path: Path | None = None) -> Path:
    """
    Downloads pac file to temporary directory
    :param url: url to pac file
    :param path: path to the location where the downloaded file will be saved.
    Will be saved to a temporary directory by default.
    :return: path to downloaded file
    """
    def download_hook(*args, **kwargs):
        if _downloader_state['terminate_download']:
            raise DownloadCancel()

    _downloader_state['terminate_download'] = False

    try:
        response = requests.get(
            url, stream=True, timeout=15, hooks={'response': download_hook}
        )
    except DownloadCancel:
        logger.debug('File PAC download cancelled')
        raise

    path = path or get_pac_path(url)
    with open(path, mode='wb') as pac:
        pac.write(response.content)

    return path


def terminate_download_pac_file():
    _downloader_state['terminate_download'] = True


def find_proxy(pac_file: str, url: str) -> dict[str, str]:
    """
    Finds a proxy for a URL
    :param pac_file: path to downloaded file
    :param url: target url
    :return: dict like this {'http': 'url:port', 'https': 'url:port'} or
    an empty dict if no proxy is needed
    """
    data: str = lib.ParseFile(pac_file, url).decode()
    result = json.loads(data)
    if result['Error']:
        raise GoPacException(result['Error'])

    return result["Proxy"]
