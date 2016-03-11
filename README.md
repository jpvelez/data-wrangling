# Data Cleaner and Scraper

This repo contains a cleaner, which cleans dirty data, and a scraper, which scrapes data from the web.

## Installation
To run this code, you'll need Make and Python 3.5 installed. To install the necessary python packages, it helps to install [Anaconda](https://docs.continuum.io/anaconda/install).

Once you have Anaconda, type this to make a new virtual environments with all the packages you need:
`conda create --name cleaner-scraper --file requirements.txt`

## Usage
All code is executable from a single command. Simply type:
`make all_tests`

This will make a new `data` directory, download the datasets we need to clean, clean them, and scrape the data we need. All outputted datasets live in `data`.

This project uses [GNU Make](http://blog.kaggle.com/2012/10/15/make-for-data-scientists/) to orchestrate a data pipeline, which is defined in `Makefile`. 

If you're new to Make, don't worry! It's simple. A Makefile consists of a series of tasks that take input files and product output files. For example:

```sh
clean_data/product.csv: raw_data/product.csv clean_dataset.py 
	cat raw_data/product.csv | python clean_dataset.py clean_data/product.pkl
```

`raw_data/product.csv`, `clean_dataset.py`, and `clean_data` are the input files.
`clean_data/product.csv` is the output file.
The shell command starting with `cat` is the task - it takes the first input file, `raw_data/product.csv`,
and passes it to the python module `clean_dataset.py` to produce our output file, `clean_data/product.pkl`.

To execute the task, you type:
`make clean_data/product.csv`

If the file doesn't already exist, Make will... make it for you!

(The reason that `clean_dataset.py` was passed in as an input file to the task, even though it doesn't contain
any data for the task to process, has to due with the way Make works. If you try to execute the task, but 
`clean_data/product.csv` already exists, Make will do nothing - unless the last updated timestamp of any of 
the input files is newer than the output file! Perhaps the input data changed, or the source code that converts
the input data to the output. In either case, we want Make to re-execute the task, and create a new output for us.)

If a task depends on an input file, and this input file doesn't exist on disk yet, but it _is_ defined as the output
file of another task, Make will execute that task first. By specifying dependencies in this way, you can execute an
entire workflow simply by executing the final task.

That's pretty much it!
