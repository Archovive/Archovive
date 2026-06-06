.PHONY: gifs test boundary

gifs:
	bash docs/assets/demo/build_gifs.sh

test:
	python -m pytest cli/tests -q

boundary:
	bash internal/scripts/verify_public_boundary.sh
