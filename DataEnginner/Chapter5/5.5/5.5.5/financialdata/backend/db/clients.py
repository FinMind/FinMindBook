from financialdata import config
from sqlalchemy import create_engine, engine


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}"
        f"@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect
