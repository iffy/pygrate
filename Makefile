.PHONY: help clean

help:
	@cat Makefile

#------------------------------------------------------------------------------
# removes temporary files
#------------------------------------------------------------------------------
clean:
	-find . -name "*.pyc" -exec rm {} \;
	-rm -rf _trial_temp
	-rm *.tgz
	-rm -rf MANIFEST

