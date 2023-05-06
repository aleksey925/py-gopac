import base64
import ctypes
import json
import logging
import typing as t
from pathlib import Path
from tempfile import gettempdir
from urllib.request import urlretrieve

from gopac.exceptions import DownloadCancel, GoPacException, SharedLibraryNotFound
from gopac.structures import GoStr

__all__ = ['find_proxy', 'download_pac_file', 'terminate_download_pac_file']

logger = logging.getLogger()
extension_dir = Path(__file__).parent.absolute() / 'extension'
_downloader_state = {'terminate_download': False}


def get_shared_library() -> Path:
    list_path = list(
        filter(
            lambda i: i.name.startswith('parser.') and not i.name.endswith('.h'),
            extension_dir.iterdir(),
        )
    )
    if len(list_path) != 1:
        raise SharedLibraryNotFound()
    return list_path[0]


def load_shared_lib(path: Path) -> ctypes.CDLL:
    library = ctypes.cdll.LoadLibrary(str(path))
    library.ParseFile.argtypes = [GoStr, GoStr]
    library.ParseFile.restype = ctypes.POINTER(ctypes.c_char_p)
    library.FreePointer.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    return library


lib = load_shared_lib(get_shared_library())


def get_pac_path(url: str) -> Path:
    return Path(gettempdir()) / f'{base64.b64encode(url.encode()).decode()}.pac'


def download_pac_file(url: str, path: t.Union[Path, None] = None) -> Path:
    """
    Downloads pac file
    :param url: url to pac file
    :param path: path to the location where the downloaded file will be saved.
    Will be saved to a temporary directory by default.
    :return: path to downloaded file
    """

    def download_hook(count: int, block_size: int, total_size: int) -> None:
        if get_terminate_download_flag():
            raise DownloadCancel()

    path = path or get_pac_path(url)
    reset_download_state()
    try:
        urlretrieve(url, path, reporthook=download_hook)
    except DownloadCancel:
        logger.debug('File PAC download cancelled')
        raise

    return path


def get_terminate_download_flag() -> bool:
    return _downloader_state['terminate_download']


def reset_download_state() -> None:
    _downloader_state['terminate_download'] = False


def terminate_download_pac_file() -> None:
    _downloader_state['terminate_download'] = True


def find_proxy(pac_file: Path, url: str) -> t.Dict[str, str]:
    """
    Finds a proxy for a URL
    :param pac_file: path to downloaded file
    :param url: target url
    :return: dict like this {'http': 'url:port', 'https': 'url:port'} or
    an empty dict if no proxy is needed
    """
    result_pointer = lib.ParseFile(str(pac_file), url)
    value = ctypes.c_char_p.from_buffer(result_pointer).value
    lib.FreePointer(result_pointer)
    if value is None:
        raise GoPacException('Unexpected value received')

    result = json.loads(value.decode())
    if result['Error']:
        raise GoPacException(result['Error'])

    return result['Proxy']
