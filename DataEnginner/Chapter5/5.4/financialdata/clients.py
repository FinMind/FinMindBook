import config
from sqlalchemy import create_engine, engine


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}"
        f"@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect


def get_mysql_monitor_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{config.MYSQL_MONITOR_USER}:{config.MYSQL_MONITOR_PASSWORD}"
        f"@{config.MYSQL_MONITOR_HOST}:{config.MYSQL_MONITOR_PORT}/{config.MYSQL_MONITOR_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect
