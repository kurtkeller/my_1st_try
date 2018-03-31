# vim:noet:ai:tw=76

# Makefile for often used tasks

help:
	@echo "  make clean	- remove files generated during testing"
	@echo "  make synchk	- run a small syntax check on python files"

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm 2>/dev/null || :

synchk:
	@EXITCODE=0; \
	\
	for F in $$(find . -name "*.py"); do \
	    FILEEXITCODE=0; \
	    \
	    head "$${F}" | grep -E -q "^# -\*- coding: UTF-8 -\*-"; \
	        if [ "$${?}" -ne "0" ]; then \
	            echo "coding: header missing on $$F"; \
		    FILEEXITCODE=2; \
	        fi; \
	    \
	    head "$${F}" | grep -E -q "^# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :"; \
	        if [ "$${?}" -ne "0" ]; then \
	            echo "vim: header missing on $$F"; \
		    FILEEXITCODE=2; \
	        fi; \
	    \
	    grep -E -q "[[:space:]][[:space:]]*$$" "$${F}" ; \
	        if [ "$${?}" -eq "0" ]; then \
	            echo "trailing whitespace found in $$F"; \
		    FILEEXITCODE=2; \
	        fi; \
	    \
	    if [ "$${FILEEXITCODE}" -ne "0" ]; then \
		EXITCODE=$${FILEEXITCODE}; \
	        echo ;\
	        echo ;\
	    fi; \
	done; \
	\
	exit $${EXITCODE}
