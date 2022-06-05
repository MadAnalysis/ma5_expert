.PHONY: all
all:
	make install
	python -m pip install pytest
	make test


.PHONY: install
install:
	pip install -e .


.PHONY: uninstall
uninstall:
	pip uninstall ma5_expert

.PHONY: test
test:
	pytest tests/.


.PHONY: build
build:
	python -m build


.PHONY: testpypi
testpypi:
	python3 -m twine upload --repository testpypi dist/*


.PHONY: pypi
pypi:
	twine upload dist/*







