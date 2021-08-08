from enum import Enum
import os
import pandas as pd
import urllib.request

from race_data import population_by_demographic as pbd

"""
Data source:
https://www.ojjdp.gov/ojstatbb/crime/ucr.asp?table_in=1
https://www.ojjdp.gov/ojstatbb/crime/ucr.asp?table_in=2
"""


def str_num_to_int(num):
    if isinstance(num, str):
        return int(num.replace(',', ''))

    return num


class DataSet(Enum):
    RACE = "race"
    AGE = "age"


metadata = {
    DataSet.RACE: {
        "url": "https://www.ojjdp.gov/ojstatbb/crime/ucr.asp?table_in=2",
        "dir": "cache/race",
        "table": "race_data"
    },
    DataSet.AGE: {
        "url": "https://www.ojjdp.gov/ojstatbb/crime/ucr.asp?table_in=1",
        "dir": "cache/age",
        "table": "age_data"
    }
}


class CrimeDataService:
    YEAR_SERIES = list(range(1980, 2020))

    def __init__(self):
        pass

    ###########################################################################
    # Methods to extract the data
    ###########################################################################

    @staticmethod
    def get_all_data(data_set: DataSet) -> pd.DataFrame:
        df = CrimeDataService.get_data_for_year(data_set, 1980)

        for year in CrimeDataService.YEAR_SERIES[1:]:
            next_df = CrimeDataService.get_data_for_year(data_set, year)
            df = pd.concat([df, next_df])

        return df

    @staticmethod
    def get_data_for_year(data_set, year: int) -> pd.DataFrame:
        cache_contents = os.listdir(metadata[data_set]['dir'])
        file_name = CrimeDataService.get_file_name(year)

        if file_name in cache_contents:
            return CrimeDataService.get_data_from_cache(data_set, year)
        else:
            return CrimeDataService.get_data_from_web(data_set, year)

    @staticmethod
    def get_data_from_cache(data_set, year: int) -> pd.DataFrame:
        file_name = CrimeDataService.get_file_name(year)
        cache_file = f"{metadata[data_set]['dir']}/{file_name}"
        df = pd.read_csv(cache_file)

        if data_set == DataSet.RACE:
            df = CrimeDataService.transform_race(df, year)
        elif data_set == DataSet.AGE:
            df = CrimeDataService.transform_age(df, year)

        return df

    @staticmethod
    def get_data_from_web(data_set, year: int) -> pd.DataFrame:
        url = CrimeDataService.get_url(data_set, year)
        file_name = CrimeDataService.get_file_name(year)
        response = urllib.request.urlopen(url)
        cache_file = f"{metadata[data_set]['dir']}/{file_name}"

        with open(cache_file, "w") as f:
            # First three lines are not CSV data
            lines = [line.decode('utf-8') for line in response.readlines()][2:]
            [f.write(line) for line in lines]

        df = pd.read_csv(cache_file)

        if data_set == DataSet.RACE:
            df = CrimeDataService.transform_race(df, year)
        elif data_set == DataSet.AGE:
            df = CrimeDataService.transform_age(df, year)

        return df

    @staticmethod
    def get_url(data_set, year: int) -> str:
        return f"{metadata[data_set]['url']}" + \
               f"&selYrs={year}&rdoGroups=1&rdoData=c&export=yes"

    @staticmethod
    def get_file_name(year: int) -> str:
        return f"{year}data.csv"

    ###########################################################################
    # Methods to transform the data
    ###########################################################################

    @staticmethod
    def transform_race(df: pd.DataFrame, year: int) -> pd.DataFrame:
        # Make a deep copy of the data frame before transforming it
        copy = pd.DataFrame.copy(df, True)
        # Only first 30 rows are valid data, so slice them from the set
        copy = copy.iloc[:31]
        # Convert whole number string columns to int
        copy['All races'] = copy['All races'].transform(str_num_to_int)
        copy['White'] = copy['White'].transform(str_num_to_int)
        copy['Black'] = copy['Black'].transform(str_num_to_int)
        copy['American Indian'] = copy['American Indian'].transform(str_num_to_int)
        copy['Asian'] = copy['Asian'].transform(str_num_to_int)
        # Add Year column
        copy['Year'] = [year] * 31
        # Drop NaN columns
        copy.dropna(axis='columns', how='all', inplace=True)
        # Add population percentage and crime percentage columns
        copy['% White Pop.'] = [CrimeDataService.get_demographic_data(year)['White'][0]] * 31
        copy['% White Crimes'] = CrimeDataService.get_crimes_percentage(copy, 2)
        copy['% Black Pop.'] = [CrimeDataService.get_demographic_data(year)['Black'][0]] * 31
        copy['% Black Crimes'] = CrimeDataService.get_crimes_percentage(copy, 3)
        copy['% American Indian Pop.'] = [CrimeDataService.get_demographic_data(year)['American Indian'][0]] * 31
        copy['% American Indian Crimes'] = CrimeDataService.get_crimes_percentage(copy, 4)
        copy['% Asian Pop.'] = [CrimeDataService.get_demographic_data(year)['Asian'][0]] * 31
        copy['% Asian Crimes'] = CrimeDataService.get_crimes_percentage(copy, 5)

        return copy

    @staticmethod
    def get_crimes_percentage(df: pd.DataFrame, col_idx: int) -> list[float]:
        def get_ratio(subset: str, total: str) -> float:
            ratio = str_num_to_int(subset) / str_num_to_int(total)
            return round(ratio * 100, 2)

        return [get_ratio(df.iloc[row, col_idx], df.iloc[row, 1])
                for row in list(range(0, 31))]

    @staticmethod
    def get_demographic_data(year: int) -> pd.DataFrame:
        if year in range(1980, 1990):
            return pbd[1980]

        if year in range(1990, 2000):
            return pbd[1990]

        if year in range(2000, 2010):
            return pbd[2000]

        if year in range(2010, 2020):
            return pbd[2010]

    @staticmethod
    def transform_age(df: pd.DataFrame, year: int) -> pd.DataFrame:
        copy = pd.DataFrame.copy(df, True)
        # Only first 30 rows are valid data, so slice them from the set
        copy = copy.iloc[:31]
        # Add Year column
        copy['Year'] = [year] * 31
        # Drop NaN columns
        copy.dropna(axis='columns', how='all', inplace=True)
        # Convert whole number string columns to int
        copy['All ages'] = copy['All ages'].transform(str_num_to_int)
        copy['0 to 17'] = copy['0 to 17'].transform(str_num_to_int)
        copy['18 & older'] = copy['18 & older'].transform(str_num_to_int)
        copy['10 to 17'] = copy['10 to 17'].transform(str_num_to_int)
        copy['0 to 14'] = copy['0 to 14'].transform(str_num_to_int)
        copy['15 to 17'] = copy['15 to 17'].transform(str_num_to_int)
        copy['18 to 20'] = copy['18 to 20'].transform(str_num_to_int)
        copy['21 to 24'] = copy['21 to 24'].transform(str_num_to_int)
        copy['25 & older'] = copy['25 & older'].transform(str_num_to_int)

        return copy
