# CrimeDataETL
Here is a simple example of an ETL data pipeline using Pandas. It could be used to analyze crime trends by race or by age. Sources for data sets are in code.

Here's how it works:

1. Load data into Pandas data frames from public source. Use a local cached copy or download the CSV to cache directory and then read from it.
2. For racial data, combine the crime data with another data set of population percentage by race
3. Transform the data: remove null columns, add year column which is not present in data set, convert strings to numbers
4. Load the data from Pandas dataframes into an SQL database

If you were going to use this for data analysis, all you would need to do is set up your DB and run the ETL script passing in your connection string.

There is a Jupyter Notebook in the `src` directory you can try out to test the extract/transform steps. Loading requires the DB to be set up.
