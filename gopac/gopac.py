import os
import sys
import json
import subprocess

from functools import lru_cache
from locale import getdefaultlocale
from os.path import dirname, abspath, join

from gopac.exceptions import CliNotFound, ErrorDecodeOutput, GoPacException

__all__ = ['find_proxy']

EXTENSION_DIR = join(dirname(abspath(__file__)), 'extension')
ENCODING = (
    'cp866' if sys.platform in ('win32', 'cygwin') else
    (getdefaultlocale()[1] if getdefaultlocale()[1] else 'UTF-8')
)


def find_shared_library():
    shared_library = os.listdir(EXTENSION_DIR)
    if len(shared_library) != 1:
        raise CliNotFound("CLI not found")
    return join(EXTENSION_DIR, shared_library[0])


@lru_cache(maxsize=None)
def find_proxy(pac_path: str, url: str, encoding=None):
    """
    Вычисляет какой proxy необходимо использовать для переданного url
    :param pac_path: путь к pac фалу
    :param url: ссылка на сайт
    :param encoding: кодировка консоли
    :return: словарь вида {'http': 'url:port', 'https': 'url:port'} или пуcтой
    словарь, если прокси не требуется
    """
    cmd = ' '.join(
        (find_shared_library(), f'-pacPath {pac_path}', f'-url {url}')
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
        raise ErrorDecodeOutput('Не удалось определить кодировку строки')
    except Exception as e:
        raise GoPacException('Возникла непредвиденная ошибка', e)

    if res.startswith("marshal error"):
        raise GoPacException(
            'Внешняя бибилиотека не смогла сфрпмировать ответ'
        )
    else:
        res = json.loads(res)

        if res['Error']:
            raise GoPacException(res['Error'])

        return res['Proxy']


if __name__ == '__main__':
    proxy = find_proxy(
        'https://antizapret.prostovpn.org/proxy.pac',
        'http://ya.ru'
    )
    print(proxy)
