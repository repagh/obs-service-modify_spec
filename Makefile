prefix = /usr

servicedir = ${prefix}/lib/obs/service

all:

install:
	install -d $(DESTDIR)$(servicedir)
	install -m 0755 modify_spec $(DESTDIR)$(servicedir)
	install -m 0644 modify_spec.service $(DESTDIR)$(servicedir)

test:
	flake8 modify_spec tests/
	python -m unittest discover tests/

clean:
	find -name "*.pyc" -exec rm {} \;
	find -name '*.pyo' -exec rm {} \;
	rm -rf modify_specc

.PHONY: all install
