from setuptools import setup, Extension

setup(
    name='pygopac',
    version='0.2.0',
    url='https://github.com/aleksey925/py-gopac',
    license='MIT',
    author='Aleksey Petrunnik',
    author_email='petrunnik.a@gmail.com',
    description='Simple library for parsing pac files.',
    packages=['gopac'],
    python_requires='>=3.8, <3.12',
    install_requires=['requests>=2.18.4'],
    setup_requires=['setuptools-golang-cli', 'wheel'],
    dependency_links=[
        'git+https://github.com/aleksey925/setuptools-golang-cli.git@0.0.3#egg=setuptools-golang-cli'
    ],
    ext_modules=[
        Extension(
            'gopac.extension.gopaccli',
            ['extension/src/gopaccli/gopaccli.go']
        ),
    ],
    build_golang_cli={'root': 'extension'},
)
