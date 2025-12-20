import pandas as pd
from fastapi import FastAPI
from sqlalchemy import (
    create_engine,
)
from api import config


def get_mysql_financialdata_engine():
    address = (
        f"mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}"
        f"@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    return engine


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price(
    stock_id: str = "",
    start_date: str = "",
    end_date: str = "",
):
    sql = f"""
    select * from TaiwanStockPrice
    where StockID = '{stock_id}'
    and Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    mysql_engine = (
        get_mysql_financialdata_engine()
    )
    data_df = pd.read_sql(
        sql, con=mysql_engine
    )
    data_dict = data_df.to_dict(
        "records"
    )
    return {"data": data_dict}
