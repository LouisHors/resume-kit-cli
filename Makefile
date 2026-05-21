PYTHON ?= python3
PREFIX ?= $(HOME)/.local/bin
PROJECT_ROOT := $(shell pwd)

.PHONY: test install-local

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover tests -v

install-local:
	mkdir -p "$(PREFIX)"
	printf '#!/usr/bin/env bash\nexec $(PYTHON) "$(PROJECT_ROOT)/resume_kit/cli.py" "$$@"\n' > "$(PREFIX)/resume-kit"
	chmod +x "$(PREFIX)/resume-kit"
	@echo "Installed $(PREFIX)/resume-kit"
