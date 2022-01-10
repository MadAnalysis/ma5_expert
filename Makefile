.PHONY: all
all:
	make install


.PHONY: install
install:
	pip install -e .


.PHONY: uninstall
uninstall:
	pip uninstall ma5_expert


