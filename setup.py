from setuptools import setup, Extension

setup(
    name='gopac',
    version='0.0.4',
    url='https://bitbucket.org/alex925/gopac/src/master/',
    author='Aleksey Petrunnik',
    author_email='zzz_vvv.94@mail.ru',
    description='',
    packages=['gopac'],
    install_requires=['requests>=2.18.4'],
    setup_requires=['setuptools-golang-cli'],
    dependency_links=[
        'git+https://alex925@bitbucket.org/alex925/setuptools-golang-cli.git@master#egg=setuptools-golang-cli'
    ],
    ext_modules=[
        Extension(
            'gopac.extension.gopaccli',
            ['extension/src/gopaccli/gopaccli.go']
        ),
    ],
    build_golang_cli={'root': 'extension'},
)
