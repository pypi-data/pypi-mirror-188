import pandas as pd
import duckdb
from datetime import datetime
import pytz
from pyarrow.parquet import ParquetFile
import pyarrow as pa 



class SCD2():
    def __init__(self) -> None:
        self.duck = duckdb.connect()


    @staticmethod
    def _create_time_parts(tz):
        if tz:
            tz = pytz.timezone(tz)
        now = datetime.now(tz)
        now_parts = [str(i) for i in[now.year, now.month, now.day, now.hour, now.minute, now.second]]
        return ",".join(now_parts)


    def _scd_queries(self, time_parts):

        # rows that are in both target and source, and active
        ### unchanged_active_keys (active - old) ###
        self.duck.execute("""
            CREATE TABLE unchanged_active_keys as 
            SELECT *
            FROM target_scd
            WHERE is_active = True
            and exists(
                SELECT * 
                FROM source_scd
                WHERE target_scd.hash = source_scd.hash
            )
            """)
        
        # rows that are in the target but no longer in the source, and are inactive
        ### unchanged_inactive_keys (inactive - old) ###
        self.duck.execute("""
            CREATE TABLE unchanged_inactive_keys as 
            SELECT * 
            FROM target_scd
            WHERE is_active = False
            and not exists(
                SELECT * 
                FROM source_scd
                WHERE target_scd.hash = source_scd.hash
            )
            """)

        # rows that are in the target but no longer in the source, and are active
        ### ended_keys (inactive - new) ###
        self.duck.execute(f"""
        CREATE TABLE ended_keys as 
        SELECT * EXCLUDE (end_ts, is_active),
        make_timestamp({time_parts}) as end_ts,
        FALSE as is_active,
        FROM target_scd
        WHERE is_active = True
        and not exists (
            SELECT * 
            FROM source_scd
            WHERE target_scd.hash = source_scd.hash
        )
        """)

        # rows that are in the source but not in the target
        ### new_keys (active - new) ###
        self.duck.execute(f"""
        CREATE TABLE new_keys as 
        SELECT *,
        make_timestamp({time_parts}) as start_ts,
        null as end_ts,
        TRUE as is_active,
        FROM source_scd
        WHERE not exists (
            SELECT * 
            FROM target_scd
            WHERE target_scd.hash = source_scd.hash
        )
        """)

        self.duck.execute("""
        CREATE TABLE final as 
        SELECT * EXCLUDE(hash) FROM unchanged_active_keys
        UNION ALL BY NAME 
        SELECT * EXCLUDE(hash) FROM unchanged_inactive_keys
        UNION ALL BY NAME
        SELECT * EXCLUDE(hash) FROM ended_keys
        UNION ALL BY NAME
        SELECT * EXCLUDE(hash) FROM new_keys
        """)


    def pandas_scd2(self, src: pd.DataFrame, tgt: pd.DataFrame, cols_to_track: list=None, tz: str=None) -> pd.DataFrame:
        """"
        src: pandas dataframe with the source of the SCD
        tgt: pandas dataframe with the target of the SCD (target can be empty)
        cols_to_track: list of columns to track changes (default is all columns from the source table)
        tz: pytz time zone to use on start_ts and end_ts, default is None (will use local time)
        the return dataframe contain the entire target table with the new changes, ready for insert overwrite of the current target table
        """

        if not cols_to_track:
            cols_to_track = list(src.columns)

        if not isinstance(cols_to_track, list):
            raise TypeError('cols_to_track must be of type list')


        time_parts = self._create_time_parts(tz)
        self.duck.execute(f"CREATE TABLE source_scd AS SELECT *, md5(concat_ws('_', {','.join(cols_to_track)})) as hash FROM src")
        self.duck.execute(f"CREATE TABLE target_scd as SELECT *, md5(concat_ws('_', {','.join(cols_to_track)})) as hash FROM tgt")

        self._scd_queries(time_parts)
        
        df = self.duck.execute("select * from final").fetch_df()    
        return df


    def parquet_scd2(self, src: str, tgt: str, cols_to_track: list=None, tz: str=None) -> None:
        """"
        src: path to the source of the SCD
        tgt: path to the target of the SCD (target can be empty)
        cols_to_track: list of columns to track changes (default is all columns from the source table)
        tz: pytz time zone to use on start_ts and end_ts, default is None (will use local time)
        tgt parquet will be overwritten
        """

        if not cols_to_track:
            pf = ParquetFile(src) 
            first_ten_rows = next(pf.iter_batches(batch_size = 1)) 
            df = pa.Table.from_batches([first_ten_rows]).to_pandas() 
            cols_to_track = list(df.columns)

        if not isinstance(cols_to_track, list):
            raise TypeError('cols_to_track must be of type list')


        time_parts = self._create_time_parts(tz)
        self.duck.execute(f"CREATE TABLE source_scd AS SELECT *, md5(concat_ws('_', {','.join(cols_to_track)})) as hash FROM '{src}'")
        self.duck.execute(f"CREATE TABLE target_scd as SELECT *, md5(concat_ws('_', {','.join(cols_to_track)})) as hash FROM '{tgt}'")

        self._scd_queries(time_parts)
        
        self.duck.execute(f"COPY (SELECT * FROM final) TO '{tgt}' (FORMAT 'parquet')")
        
