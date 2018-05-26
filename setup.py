from setuptools import setup, Extension

setup(
    name='gopac',
    version='0.0.1',
    url='',
    license='',
    author='Aleksey Petrunnik',
    author_email='',
    description='',
    packages=['gopac'],
    setup_requires=['setuptools-golang-cli'],
    ext_modules=[
        Extension(
            'gopac.extension.gopaccli',
            ['extension/src/gopaccli/gopaccli.go']
        ),
    ],
    build_golang_cli={'root': 'extension'},
)
