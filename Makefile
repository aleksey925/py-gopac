build-whl:
	pdm build

pip-build-whl:
	pip wheel --no-deps --wheel-dir ./dist .
