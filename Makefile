.PHONY: clean env docs

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

env:
	conda env create -p ./env -f environment.yml

docs:
	$(MAKE) -C ./docsrc github