build-dist-by-pdm:
	pdm build

build-dist:
	python -m build . --sdist && \
	pip wheel --no-deps --wheel-dir ./dist .
