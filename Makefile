data/test.csv:
	mkdir -p data
	curl -o $@ https://s3.amazonaws.com/data-code-test/test.csv

data/clean_test.csv: data/test.csv clean_data.py
	python clean_data.py $< $@

