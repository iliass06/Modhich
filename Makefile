# Makefile [cite: 83]

install: # [cite: 86]
	pip install -e ./mazegen
	pip install flake8 mypy

run: # [cite: 87]
	python3 a_maze_ing.py config.txt

debug: # [cite: 88]
	python3 -m pdb a_maze_ing.py config.txt

clean: # [cite: 89]
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf mazegen/build mazegen/dist mazegen/*.egg-info

lint: # [cite: 92, 94]
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict: # [cite: 95]
	flake8 .
	mypy --strict .