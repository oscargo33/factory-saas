PYTHON ?= python3

.PHONY: docs-sync docs-check

docs-sync:
	DOCS_SYNC_DATE=$$(date +%F) $(PYTHON) scripts/docs/sync_docs_versioning.py

docs-check:
	$(PYTHON) scripts/docs/sync_docs_versioning.py --check