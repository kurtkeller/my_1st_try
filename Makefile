# vim:noet:ai:tw=76

# Makefile for often used tasks

help:
	@echo "  make clean	- remove files generated during testing"

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm 2>/dev/null || :
