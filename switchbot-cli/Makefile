.PHONY: install
install:
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python3 get-pip.py
	rm get-pip.py
	python3 -m pip install -r requirements.txt

.PHONY: setup
setup:
	python3 src/main.py setup

.PHONY: run
run:
	python3 src/main.py