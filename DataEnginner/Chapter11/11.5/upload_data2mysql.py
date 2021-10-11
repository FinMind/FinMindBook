import pandas as pd
import io
import sys
from loguru import logger
from sqlalchemy import (
    create_engine,
    engine,
)
from tqdm import tqdm
import requests


def get_mysql_financialdata_conn() -> engine.base.Connection:
    # TODO 請將 IP 換成讀者自己的 IP
    address = "mysql+pymysql://root:test@139.162.104.54:3306/FinancialData"
    engine = create_engine(address)
    connect = engine.connect()
    return connect


def create_taiwan_stock_info_sql():
    return """
        CREATE TABLE `taiwan_stock_info` (
            `industry_category` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
            `stock_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
            `stock_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
            `type` varchar(4) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '上市twse/上櫃tpex',
            `date` date DEFAULT NULL,
            PRIMARY KEY (`stock_id`,`industry_category`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
    """


def create_taiwan_stock_price_sql():
    return """
        CREATE TABLE `taiwan_stock_price` (
            `StockID` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
            `Transaction` bigint NOT NULL,
            `TradeVolume` int NOT NULL,
            `TradeValue` bigint NOT NULL,
            `Open` float NOT NULL,
            `Max` float NOT NULL,
            `Min` float NOT NULL,
            `Close` float NOT NULL,
            `Change` float NOT NULL,
            `Date` date NOT NULL,
            PRIMARY KEY(`StockID`, `Date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci
        PARTITION BY KEY (StockID)
        PARTITIONS 10;
    """


def create_taiwan_stock_institutional_investors_sql():
    return """
        CREATE TABLE taiwan_stock_institutional_investors(
            `name` VARCHAR(20),
            `buy` BIGINT(64),
            `sell` BIGINT(64),
            `stock_id` VARCHAR(10),
            `date` DATE,
            PRIMARY KEY(`stock_id`, `date`, `name`)
        ) PARTITION BY KEY(`stock_id`) PARTITIONS 10;
    """


def create_taiwan_stock_margin_purchase_short_sale_sql():
    return """
        CREATE TABLE `taiwan_stock_margin_purchase_short_sale`(
            `stock_id` VARCHAR(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '股票代碼',
            `MarginPurchaseBuy` BIGINT NOT NULL COMMENT '融資買進',
            `MarginPurchaseSell` BIGINT NOT NULL COMMENT '融資賣出',
            `MarginPurchaseCashRepayment` BIGINT NOT NULL COMMENT '融資現金償還',
            `MarginPurchaseYesterdayBalance` BIGINT NOT NULL COMMENT '融資昨日餘額',
            `MarginPurchaseTodayBalance` BIGINT NOT NULL COMMENT '融資今日餘額',
            `MarginPurchaseLimit` BIGINT NOT NULL COMMENT '融資限額',
            `ShortSaleBuy` BIGINT NOT NULL COMMENT '融券買進',
            `ShortSaleSell` BIGINT NOT NULL COMMENT '融券賣出',
            `ShortSaleCashRepayment` BIGINT NOT NULL COMMENT '融券償還',
            `ShortSaleYesterdayBalance` BIGINT NOT NULL COMMENT '融券昨日餘額',
            `ShortSaleTodayBalance` BIGINT NOT NULL COMMENT '融券今日餘額',
            `ShortSaleLimit` BIGINT NOT NULL COMMENT '融券限制',
            `OffsetLoanAndShort` BIGINT DEFAULT NULL COMMENT '資券互抵',
            `date` DATE NOT NULL COMMENT '日期',
            PRIMARY KEY(`stock_id`, `date`)
        ) PARTITION BY KEY(`stock_id`) PARTITIONS 10;
    """


def create_taiwan_stock_holding_shares_per_sql():
    return """
        CREATE TABLE taiwan_stock_holding_shares_per (
            `HoldingSharesLevel` VARCHAR(19),
            `people` INT(10),
            `unit` BIGINT(64),
            `percent` FLOAT,
            `stock_id` VARCHAR(10),
            `date` DATE,
            `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`stock_id`,`date`,`HoldingSharesLevel`)
        )
        PARTITION BY KEY(stock_id)
        PARTITIONS 10;
    """


def create_table(
    table: str,
    mysql_conn: engine.base.Connection,
):
    sql = eval(f"create_{table}_sql()")
    try:
        logger.info(
            f"create table {table}"
        )
        mysql_conn.execute(sql)
    except:
        logger.info(
            f"{table} already exists"
        )


def download_data(
    table: str,
    mysql_conn: engine.base.Connection,
):
    chunk_size = 10000
    logger.info("download data")
    url = f"https://github.com/FinMind/FinMindBook/releases/download/data/{table}.csv"
    resp = requests.get(
        url, stream=True
    )
    int(resp.headers["content-length"])
    text = ""
    for data in tqdm(
        resp.iter_content(
            chunk_size=chunk_size
        )
    ):
        text += data.decode("utf-8")
    df = pd.read_csv(io.StringIO(text))
    logger.info(
        "download data complete"
    )
    try:
        logger.info("upload to mysql")
        count = (
            int(len(df) / chunk_size)
            + 1
        )
        for i in tqdm(range(count)):
            df[
                (i * chunk_size) : (
                    i + 1
                )
                * chunk_size
            ].to_sql(
                name=table,
                con=mysql_conn,
                if_exists="append",
                index=False,
            )
    except:
        logger.info("already upload")


def main(table: str):
    mysql_conn = (
        get_mysql_financialdata_conn()
    )
    create_table(
        table=table,
        mysql_conn=mysql_conn,
    )
    download_data(
        table=table,
        mysql_conn=mysql_conn,
    )


if __name__ == "__main__":
    table = sys.argv[1]
    main(table)
