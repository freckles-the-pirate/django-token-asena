
.PHONY: test
test:
	cd tests; \
	./runall.sh;

.PHONY: clean
clean:
	for f in $(shell find -iname '*.pyc'); do \
		rm -fr $$f; \
	done;
