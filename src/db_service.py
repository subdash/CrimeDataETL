from sqlalchemy import create_engine
import pandas as pd

from crime_data import DataSet, metadata


class DBService:
    def __init__(self, conn_string):
        # conn_string: mysql://{user}:{password}@localhost/{database}"
        engine = create_engine(conn_string)
        self.conn = engine.connect()

    def load_data(self, df: pd.DataFrame, data_set: DataSet):
        copy = DBService.prepare_to_load(df)
        table_name = metadata[data_set]['table']
        copy.to_sql(table_name, con=self.conn)

    @staticmethod
    def prepare_to_load(df: pd.DataFrame) -> pd.DataFrame:
        copy = pd.DataFrame.copy(df, True)
        copy.columns = [DBService.make_sql_col_name(col)
                        for col in copy.columns]
        copy.reset_index(drop=True, inplace=True)
        return copy

    @staticmethod
    def make_sql_col_name(col: str) -> str:
        return col.lower() \
            .replace(' ', '_') \
            .replace('%', 'percent') \
            .replace('&', 'and') \
            .replace('.', '')
