tests:
	python -m unittest discover -s tests/

startup-daemon:
	python -u run.py&

setup:
	echo "Not yet implemented"

.PHONY: tests startup-daemon setup
