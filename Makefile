ifeq ($(OS),Windows_NT)
    ACTIVATE=venv\Scripts\activate.bat
    PYTHON=venv\Scripts\python.exe
    PIP=venv\Scripts\pip.exe
    SHELL=cmd
    .SHELLFLAGS=/C
else
    ACTIVATE=. venv/bin/activate
    PYTHON=venv/bin/python
    PIP=venv/bin/pip
    SHELL=/bin/bash
    .SHELLFLAGS=-c
endif

build:
	@echo "Building frontend..."
	npm run build

run:
	@echo "Running application..."
	$(ACTIVATE) && $(PYTHON) entrypoint.py

dev:
	@echo "Starting dev server..."
	npm run dev

install:
	@echo "Setting up Python virtual environment..."
	./setup.sh
	@echo "Activating virtual environment and installing Python dependencies..."
	$(ACTIVATE) && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt
	@echo "Installing frontend dependencies..."
	npm install --no-audit --no-fund
	@echo "Building frontend..."
	npm run build

start:
	@echo "Setting up Python virtual environment..."
	./setup.sh
	@echo "Activating virtual environment and installing Python dependencies..."
	$(ACTIVATE) && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt
	@echo "Installing frontend dependencies..."
	npm install --no-audit --no-fund
	@echo "Building frontend..."
	npm run build
	@echo "Starting application..."
	$(ACTIVATE) && $(PYTHON) entrypoint.py
