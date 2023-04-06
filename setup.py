from setuptools import setup, Extension

setup(
    # See pyproject.toml for most of the config metadata
    packages=['gopac'],
    ext_modules=[
        Extension(
            'gopac.extension.parser',
            ['extension/src/parser/main.go']
        ),
    ],
    build_golang={'root': 'extension'},
)
