tests:
	python -m unittest discover -s tests/

startup-daemon:
	nohup python -u run.py&

.PHONY: tests startup-daemon
