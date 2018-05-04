# Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2018  Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

.PHONY: make show-all rm_pyc doc_clean doc man coverage test dist \
	install install-pip  install-src install-metafiles \
	uninstall-metafiles uninstall clean

DESTDIR			= /
DESKTOP_PATH		= $(DESTDIR)/usr/share/applications
ICON_PATH		= $(DESTDIR)/usr/share/icons/hicolor
MAN_PATH		= $(DESTDIR)/usr/share/man/man1
INFO_PATH		= $(DESTDIR)/usr/share/info
ZSH_SITE_FUNCS_PATH	= $(DESTDIR)/usr/share/zsh/site-functions
PYTHON_EXEC		= python
PIP_EXEC		= pip

VERSION		= 0.4.0.dev0

# Include any local configuration overrides
sinclude config.mk

make:
	@echo 'make install'
	@echo 'make uninstall'
	@echo '  Install python package, scripts and metafiles'
	@echo
	@echo 'make install-metafiles'
	@echo 'make uninstall-metafiles'
	@echo '  Install or remove Zsh completion manpage, info document and logos '
	@echo '  (does not install python package and scripts)'
	@echo
	@echo 'make show-all'
	@echo '  Show development/packaging targets'

show-all: make
	@echo
	@echo
	@echo 'TARGETS FOR DISTRIBUTION PACKAGE(R)S'
	@echo 'make install-pip    install wdocker wheel pkg with pip (default)'
	@echo 'make install-src    install via setup.py install --root=$$DESTDIR'
	@echo
	@echo 'Note: make install-src does not install requirements.txt and '
	@echo '      is aimed for usage in creating distribution packages'
	@echo
	@echo "DEVELOPMENT TARGETS"
	@echo "make test      Run unittests, check-manifest and flake8"
	@echo "make doc       Build html documentation with Sphinx"
	@echo "make man       Build manpage and info documentation with Sphinx"
	@echo "make dist      Build python source archive file"
	@echo "make clean     Clean program build files"
	@echo "make coverage  Run coverage with nosetests (experimental)"

rm_pyc:
	find . -name "*.pyc" | xargs /bin/rm -f

doc_clean: rm_pyc
	cd docs/en/; make clean

doc: doc_clean
	cd docs/en/; make html
	rm -rf doc/html/$(VERSION)
	mkdir -p doc/html/$(VERSION)
	mv docs/en/_build/html doc/html/$(VERSION)/en
	make doc_clean
	cd doc/html/$(VERSION)/en; $(PYTHON_EXEC) -m http.server --bind 127.0.0.1

man: rm_pyc
	cd docs/man-en/; make clean
	cd docs/man-en/; make man
	mv docs/man-en/_build/man/dispass.1 .
	cd docs/man-en/; make clean
	cd docs/en/; make info
	mv docs/en/_build/texinfo/DisPass.info ./dispass.info
	make doc_clean

coverage:
	coverage erase
	coverage run .virtualenv/bin/pytest -v
	coverage report
	coverage html

test:
	pytest -v
	@echo 'DONE... All tests have passed'
	@echo
	check-manifest --ignore 'docs*'
	@echo 'DONE... Everything seems to be in the MANIFEST file'
	@echo
	flake8 dispass tests
	@echo 'DONE... All code is PEP-8 compliant'

dist: rm_pyc
	$(PIP_EXEC) install -r requirements.txt
	$(PYTHON_EXEC) setup.py sdist bdist_wheel

install: install-pip

install-pip: dist install-metafiles
	$(PIP_EXEC) install --upgrade dist/DisPass-$(VERSION)-py2.py3-none-any.whl
	install-info dispass.info $(INFO_PATH)/dir
	make clean

install-src: install-metafiles
	$(PYTHON_EXEC) setup.py install --root='$(DESTDIR)'
	make clean

install-metafiles:
	gzip -c dispass.1 > dispass.1.gz
	gzip -c dispass.info > dispass.info.gz
	install -Dm644 dispass.1.gz $(MAN_PATH)/dispass.1.gz
	install -Dm644 dispass.info.gz $(INFO_PATH)/dispass.info.gz
	install -Dm644 zsh/_dispass $(ZSH_SITE_FUNCS_PATH)/_dispass
	install -Dm644 etc/dispass.desktop $(DESKTOP_PATH)/dispass.desktop
	for size in 24 32 64 128 256 512; do \
		install -Dm644 "logo/logo$${size}.png" \
		"$(ICON_PATH)/$${size}x$${size}/apps/dispass.png"; \
	done

uninstall-metafiles:
	rm -f $(MAN_PATH)/dispass.1.gz
	rm -f $(INFO_PATH)/dispass.info.gz
	rm -f $(ZSH_SITE_FUNCS_PATH)/_dispass
	rm -f $(DESKTOP_PATH)/dispass.desktop
	for size in 24 32 64 128 256 512; do \
		rm -f "$(ICON_PATH)/$${size}x$${size}/apps/dispass.png"; \
	done

uninstall: clean uninstall-metafiles
	$(PIP_EXEC) uninstall dispass

clean:
	rm -f MANIFEST dispass.1.gz dispass.info.gz
	rm -rf build dist DisPass.egg-info

# vim: set noet ts=8 sw=8 sts=8:
