tests:
	python -m unittest discover -s tests/

linux-startup: #starts bpbot in the background, outputting everything to log.txt
	nohup python -u run.py </dev/null >log.txt 2>&1 &


.PHONY: tests startup
