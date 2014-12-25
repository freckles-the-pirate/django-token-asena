BASE_DIR=asena

PIP=`which pip`

.PHONY: install
install:
	$(PIP) install . -U

.PHONY: test
test:
	./runtests.sh $(BASE_DIR)

.PHONY: clean
clean:
	for f in $(shell find -iname '*.pyc'); do \
		rm -fr $$f; \
	done;