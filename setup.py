from setuptools import Extension, find_packages, setup

setup(
    # See pyproject.toml for most of the config metadata
    packages=['extension', *find_packages()],
    package_data={'extension': ['src/parser/*']},
    ext_modules=[
        Extension('gopac.extension.parser', ['extension/src/parser/main.go']),
    ],
    build_golang={'root': 'extension'},
)
