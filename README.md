# Historical distance
The goal of this repository is to calculate the historical distance in days between the publication dates of the texts in a co-referential corpus and the event date of the event that they refer to. It returns a data frame, but exports to excel when specified. When the publication date of the text could not be retrieved, 'unknown' is returned. When an event date is outside of the lower bound of panda's time frame, it uses this lower bound as the default event date.

## Prerequisites
Python 3.7.4 was used to create this package. It might work with older versions of Python.

## Installing
A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```

## Usage
Step 1: enter the test folder and place your folder with the collection of reference texts in NAF format.
Step 2: enter test.py and adapt any variable to your needs, e.g. the folder title in the filepath, the time buckets etc.
Step 3: run test.py from the command line.
The function calculate_historical_distance returns a pandas dataframe. If an output folder is specified, then the function creates an excel file there.

## Authors
* **Levi Remijnse** (l.remijnse@vu.nl)
