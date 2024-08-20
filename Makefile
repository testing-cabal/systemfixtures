# These paths are valid on Debian-based systems, on other systems you
# might have to set these variables from the command line.
COVERAGE ?= python3-coverage
SPHINXBUILD ?= /usr/share/sphinx/scripts/python3/sphinx-build

SOURCE = systemfixtures

all: check check-doc

check:
	rm -f .coverage
	$(COVERAGE) run --source=$(SOURCE) -m testtools.run discover
	$(COVERAGE) report -m --fail-under=100 --rcfile=.coveragerc.py3

check-doc:
	SPHINXBUILD=$(SPHINXBUILD) $(MAKE) -C doc doctest

dependencies:
	sudo apt-get install \
		python3-pbr \
		python3-fixtures \
		python3-testtools \
		python3-requests-mock \
		python3-fakesleep \
		python3-coverage \
		python3-sphinx

clean:
	rm -rf $(SOURCE).egg-info dist
	rm -f AUTHORS ChangeLog
	find -type f -name "*.pyc" | xargs rm -f
	find -type d -name "__pycache_" | xargs rm -rf

.PHONY: all check check-doc dependencies
