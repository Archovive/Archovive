.PHONY: demo run test boundary ci-demo dgpp

PY ?= python3
REPO_ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

demo run:
	bash dist/install.sh

ci-demo:
	@$(PY) -m pip install -q -e internal/ 2>/dev/null || \
	  $(PY) -m pip install -q --break-system-packages -e internal/
	@export PATH="$(REPO_ROOT)dist:$$PATH" && \
	  archovive ci check --repo examples/demo-fintech

test:
	@$(PY) -m pip install -q -e internal/ 2>/dev/null || \
	  $(PY) -m pip install -q --break-system-packages -e internal/
	$(PY) -m pytest cli/tests tests -q

boundary:
	bash internal/scripts/verify_public_boundary.sh

dgpp:
	@$(PY) -m pip install -q -e internal/ 2>/dev/null || \
	  $(PY) -m pip install -q --break-system-packages -e internal/
	$(PY) -m pytest tests/test_dgpp_governance_parity.py -v
