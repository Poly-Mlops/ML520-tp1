.DEFAULT_GOAL := help

#########################################
# VARIABLES
#########################################
UV ?= uv
RUN ?= $(UV) run
PYTHON ?= $(RUN) python

PACKAGE ?= inferapi

OUT_DIR ?= out
DATA_DIR ?= data
CSV_FILE ?= $(DATA_DIR)/dataset.csv
DATA_FILE ?= $(DATA_DIR)/dataset.parquet
MODEL_FILE ?= $(OUT_DIR)/models/model.joblib
ENV_FILE ?= .env

BIND_ADDR ?= 127.0.0.1
PORT ?= 8000

#########################################
# DEPENDENCIES
#########################################
.PHONY: install req-install

install: req-install  ## Alias for req-install

req-install:  ## Create/refresh .venv exactly from uv.lock (project installed editable)
	$(UV) sync

#########################################
# SECRETS
#########################################
.PHONY: secrets-show

# Your .env is a copy of .env.example with a real token in it - see the file itself.
secrets-show:  ## Print the local API token (for curl), never the whole file
	@grep '^ML520_SECURITY__API_TOKEN=' $(ENV_FILE) | cut -d= -f2

#########################################
# CODE QUALITY
#########################################
.PHONY: code-quality code-lint code-lint-fix code-format code-format-fix code-format-preview

code-quality:  ## Run lint and format checks, this is what will be graded
	@$(MAKE) --keep-going --no-print-directory code-lint code-format

code-lint:  ## Run lint checks
	$(RUN) ruff check

code-lint-fix:  ## Fix lint errors
	$(RUN) ruff check --fix

code-format:  ## Check code style adherence
	$(RUN) ruff format --check

code-format-fix:  ## Fix code style adherence
	$(RUN) ruff format

code-format-preview:  ## Preview the changes code-format-fix would make
	$(RUN) ruff format --check --diff

#########################################
# TESTS
#########################################
.PHONY: tests

tests:  ## Run the test suite
	$(RUN) pytest

#########################################
# DATA AND MODELS
#########################################
.PHONY: data-convert model-train

data-convert:  ## Rebuild the parquet from the CSV, whether or not it already exists
	$(RUN) $(PACKAGE) data-convert --csv $(CSV_FILE) --parquet $(DATA_FILE)

model-train: ## Train the model, write the artifact to out/models/model.joblib
	$(RUN) $(PACKAGE) train --data $(DATA_FILE) --output $(MODEL_FILE) --overwrite

#########################################
# SERVING
#########################################
.PHONY: serve serve-dev serve-debug

serve:  ## Serve the inferapi app
	$(RUN) gunicorn --workers 2 --worker-class uvicorn.workers.UvicornWorker \
		--bind $(BIND_ADDR):$(PORT) $(PACKAGE).serve:app

serve-dev:  ## DEV server for inferapi app with hot reload
	$(RUN) uvicorn $(PACKAGE).serve:app --reload --port $(PORT) --host $(BIND_ADDR)

# Waits for your editor to attach on port 5678 before importing anything, which is
# the only way to put a breakpoint in create_app() and have it hit.
serve-debug:  ## Serve under debugpy and wait for the debugger to attach (port 5678)
	$(PYTHON) -m debugpy --listen 5678 --wait-for-client \
		-m uvicorn $(PACKAGE).serve:app --port $(PORT) --host $(BIND_ADDR)

#########################################
# NOTEBOOKS
#########################################
.PHONY: notebook-launch

notebook-launch:  ## Launch JupyterLab (pulls in the `notebooks` dependency group)
	$(UV) run --group notebooks jupyter lab --no-browser

#########################################
# LAB
#########################################
.PHONY: submit

submit:  ## Bundle the full history for hand-in: make submit TEAM=<number>
	@test -n "$(TEAM)" || { echo "usage: make submit TEAM=<number>"; exit 1; }
	@mkdir -p $(OUT_DIR)
	git bundle create $(OUT_DIR)/tp1_team_$(TEAM).bundle --all
	@echo "wrote $(OUT_DIR)/tp1_team_$(TEAM).bundle"

#########################################
# HOUSEKEEPING
#########################################
.PHONY: help

# Taken from: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:  ## Show this help
	@grep -h -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

-include Makefile.teacher