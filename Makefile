BASE_DIR=asena

PIP=`which pip`
PYTHON=`which python`
FORMATS=gztar,zip

.PHONY: install
install:
	$(PIP) install . -U

.PHONY: release
release:
	$(PYTHON) setup.py sdist --formats=$(FORMATS) && \
		twine upload dist/*

.PHONY: test
test:
	./runtests.sh $(BASE_DIR)

.PHONY: clean
clean:
	for f in $(shell find -iname '*.pyc'); do \
		rm -fr $$f; \
	done;
