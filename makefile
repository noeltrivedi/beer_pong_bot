tests:
	python -m unittest discover -s tests/

startup-daemon:
	python -u run.py&

setup:
	python init_spreadsheet.py

.PHONY: tests startup-daemon setup
