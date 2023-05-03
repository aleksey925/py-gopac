from setuptools import Extension, find_packages, setup

setup(
    # See pyproject.toml for most of the config metadata
    packages=['extension', *find_packages(exclude=['tests'])],
    package_data={'extension': ['src/parser/*.go', 'src/parser/*.mod', 'src/parser/*.sum']},
    ext_modules=[
        Extension('gopac.extension.parser', ['extension/src/parser/main.go']),
    ],
    build_golang={'root': 'extension'},
)
