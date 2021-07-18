#! /usr/bin/env bash

.PHONY: clean
clean:
    rm -rf ma5_expert.egg-info/


#.PHONY: requirements
#requirements: requirements.txt
#	pip install -r requirements.txt


.PHONY: install
install:
    pip install -e .


.PHONY: all
all:
    make install


.PHONY: uninstall
uninstall:
    pip uninstall ma5_expert