PYTHON ?= python
PYTHON_MAJOR = $(shell $(PYTHON) -c "import sys; print(sys.version_info.major)")

# These paths are valid on Debian-based systems, on other systems you
# might have to set these variables from the command line.
COVERAGE ?= $(PYTHON)-coverage
SPHINXBUILD ?= /usr/share/sphinx/scripts/python$(PYTHON_MAJOR)/sphinx-build

SOURCE = systemfixtures

all: check check-doc

check:
	rm -f .coverage
	$(COVERAGE) run --source=$(SOURCE) -m testtools.run discover
	$(COVERAGE) report -m --fail-under=100 --rcfile=.coveragerc.py$(PYTHON_MAJOR)

check-doc:
	SPHINXBUILD=$(SPHINXBUILD) $(MAKE) -C doc doctest

dependencies:
	sudo apt-get install \
		$(PYTHON)-pbr \
		$(PYTHON)-fixtures \
		$(PYTHON)-testtools \
		$(PYTHON)-requests-mock \
		$(PYTHON)-fakesleep \
		$(PYTHON)-coverage \
		$(PYTHON)-sphinx

clean:
	rm -rf $(SOURCE).egg-info dist
	rm -f AUTHORS ChangeLog
	find -type f -name "*.pyc" | xargs rm -f
	find -type d -name "__pycache_" | xargs rm -rf

.PHONY: all check check-doc dependencies
