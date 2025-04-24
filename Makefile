# Makefile

VENV_DIR := .venv
REQ_FILE := requirements.txt

.PHONY: all setup-web setup-python clean

all: setup-web setup-python

setup-web:
	npm install

setup-python:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r $(REQ_FILE)

clean:
	rm -rf $(VENV_DIR) node_modules package-lock.json
