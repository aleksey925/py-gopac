build-dist-by-pdm:
	find . -maxdepth 1 -type d -name '*.egg-info' -print0 | xargs -0 rm -r && \
	pdm build

build-dist:
	find . -maxdepth 1 -type d -name '*.egg-info' -print0 | xargs -0 rm -r && \
	python -m build . --sdist && \
	pip wheel --no-deps --wheel-dir ./dist .

build-extension:
	cd extension/src/parser/ && \
	go build -buildmode=c-shared -o ../../../gopac/extension/parser.so main.go

lint:
	pre-commit run --all
