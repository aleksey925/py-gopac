import os
import sys
import json
import base64
import subprocess
from functools import lru_cache
from locale import getdefaultlocale
from os.path import dirname, abspath, join
from tempfile import gettempdir

import requests

from gopac.exceptions import (
    CliNotFound, ErrorDecodeOutput, GoPacException, DownloadCancel,
    DownloadPacFileException,
    SavePacFileException)
from gopac.logger import init_logger

__all__ = ['find_proxy', 'download_pac_file', 'terminate_download_pac_file']

EXTENSION_DIR = join(dirname(abspath(__file__)), 'extension')
ENCODING = (
    'cp866' if sys.platform in ('win32', 'cygwin') else
    (getdefaultlocale()[1] if getdefaultlocale()[1] else 'UTF-8')
)
SERVICE_INFO = {
    'pac_path': '',
    'terminate_download': False
}
LOGGER = init_logger()


def find_shared_library():
    shared_library = list(filter(
        lambda i: not i.endswith('.py'), os.listdir(EXTENSION_DIR)
    ))
    if len(shared_library) != 1:
        raise CliNotFound("CLI not found")
    return join(EXTENSION_DIR, shared_library[0])


def get_pac_path(url):
    return join(gettempdir(), base64.b64encode(url.encode()).decode()) + '.pac'


def download_pac_file(url: str) -> str:
    """
    Скачивает PAC файл во временную папку
    :param url: путь к файлу
    :return: путь к скачанному PAC файлу
    """
    def download_hook(*args, **kwargs):
        if SERVICE_INFO['terminate_download']:
            raise DownloadCancel()

    SERVICE_INFO['terminate_download'] = False

    try:
        response = requests.get(
            url, stream=True, timeout=15, hooks={'response': download_hook}
        )
    except DownloadCancel:
        LOGGER.debug('Загрузка PAC файла отменена')
        raise
    except Exception as e:
        raise DownloadPacFileException(
            'Возникла ошибка при скачивании PAC файла', e
        )

    try:
        SERVICE_INFO['pac_path'] = get_pac_path(url)
        with open(SERVICE_INFO['pac_path'], mode='wb') as pac:
            pac.write(response.content)
        return SERVICE_INFO['pac_path']
    except Exception as e:
        message = 'Ошибка при сохрании скачанного файла'
        LOGGER.error(message, exc_info=True)
        raise SavePacFileException(message, e)


def terminate_download_pac_file():
    SERVICE_INFO['terminate_download'] = True


@lru_cache(maxsize=None)
def find_proxy(pac_file: str, url: str, encoding=None) -> dict:
    """
    Вычисляет какой proxy необходимо использовать для переданного url
    :param pac_file: путь к pac фалу или URL
    :param url: ссылка на сайт
    :param encoding: кодировка консоли
    :return: словарь вида {'http': 'url:port', 'https': 'url:port'} или пустой
    словарь, если прокси не требуется
    """
    cmd = ' '.join(
        (find_shared_library(), f'-pacFile {pac_file}', f'-url {url}')
    )
    encoding = encoding if encoding else ENCODING
    try:
        res = subprocess.check_output(cmd, shell=True).decode(encoding)
    except subprocess.CalledProcessError:
        raise ValueError(
            'Переданы не корректные данные, не возможно выполнить '
            'консольную команду'
        )
    except UnicodeError:
        raise ErrorDecodeOutput(
            'Не удалось определить кодировку системной консоли и декодировать '
            'результат работы внешней программы'
        )
    except Exception as e:
        raise GoPacException('Возникла непредвиденная ошибка', e)

    if res.startswith("marshal error"):
        raise GoPacException(
            'Внешняя бибилиотека не смогла сформировать ответ'
        )
    else:
        res = json.loads(res)

        if res['Error']:
            raise GoPacException(res['Error'])

        return res['Proxy']
