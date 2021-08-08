import sys

from crime_data import CrimeDataService, DataSet
from db_service import DBService

if __name__ == '__main__':
    conn_string = sys.argv[1]
    dbs = DBService(conn_string)

    # EXTRACT data from web or local files. Apply TRANSFORMATIONS which
    # make the data suitable for SQL queries (convert string representations
    # of numbers to actual numbers, add demographic percentage columns, etc.)
    all_race_data = CrimeDataService.get_all_data(DataSet.RACE)
    all_age_data = CrimeDataService.get_all_data(DataSet.AGE)
    # LOAD data into SQL database.
    dbs.load_data(all_race_data, DataSet.RACE)
    dbs.load_data(all_age_data, DataSet.AGE)
