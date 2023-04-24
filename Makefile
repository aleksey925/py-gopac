build-whl:
	pdm build

build-whl-pip:
	pip wheel --no-deps --wheel-dir ./dist .
