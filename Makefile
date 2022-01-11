.PHONY: all
all:
	make install


.PHONY: install
install:
	pip install -e .


.PHONY: uninstall
uninstall:
	pip uninstall ma5_expert


.PHONY: build
build:
	python -m build


.PHONY: testpypi
testpypi:
	python3 -m twine upload --repository testpypi dist/*


.PHONY: pypi
pypi:
	twine upload dist/*







