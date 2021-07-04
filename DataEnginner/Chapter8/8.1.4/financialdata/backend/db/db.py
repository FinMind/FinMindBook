import pandas as pd
from loguru import logger
from sqlalchemy import engine


def upload_data(
    df: pd.DataFrame, table: str, mysql_conn: engine.base.Connection
):
    if len(df) > 0:
        try:
            df.to_sql(
                name=table,
                con=mysql_conn,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
        except Exception as e:
            logger.info(e)
