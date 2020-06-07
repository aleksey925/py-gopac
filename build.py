# Собирает whl под все атуальные версии python и подготавливает окружение для
# порогона unit тестов
import os
import re
import glob
import shutil
import subprocess as sp

from os.path import split

EXTENSION_PATH = './gopac/extension/'
SUPPORTED_PYTHON = ('34', '35', '36', '37', '38', '39')


def clean():
    for i in ('./build', './dist', EXTENSION_PATH):
        try:
            shutil.rmtree(i)
        except FileNotFoundError:
            pass
        except Exception:
            print(f'Не удалось удалить {i}')


def create_whl():
    if os.name == 'nt':
        command = 'python ./setup.py bdist_wheel'
    else:
        command = 'python3 ./setup.py bdist_wheel'

    process = sp.Popen(command, shell=True)
    process.wait()

    whl_name = glob.glob('./dist/*.whl')
    pattern = re.compile('-cp\d{2}')
    if whl_name:
        whl_name = split(whl_name[0])[1]
        for i in SUPPORTED_PYTHON:
            new_whl = pattern.sub('-cp{}'.format(i), whl_name)
            try:
                shutil.copy(f'./dist/{whl_name}', f'./dist/{new_whl}')
            except shutil.SameFileError:
                pass


def prepare_env():
    for current_path, dirs, files in os.walk('./build/'):
        for i in files:
            if current_path.endswith('extension'):
                os.mkdir(EXTENSION_PATH)
                shutil.copy(
                    os.path.join(current_path, i),
                    os.path.join(EXTENSION_PATH, i)
                )
                break


clean()
create_whl()
prepare_env()
