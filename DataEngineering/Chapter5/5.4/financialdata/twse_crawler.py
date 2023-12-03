import datetime
import sys
import time
import typing

import pandas as pd
import requests
from loguru import logger
from pydantic import BaseModel
from tqdm import tqdm

from financialdata.router import Router


def clear_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """資料清理, 將文字轉成數字"""
    df["Dir"] = (
        df["Dir"]
        .str.split(">")
        .str[1]
        .str.split("<")
        .str[0]
    )
    df["Change"] = (
        df["Dir"] + df["Change"]
    )
    df["Change"] = (
        df["Change"]
        .str.replace(" ", "")
        .str.replace("X", "")
        .astype(float)
    )
    df = df.fillna("")
    df = df.drop(["Dir"], axis=1)
    for col in [
        "TradeVolume",
        "Transaction",
        "TradeValue",
        "Open",
        "Max",
        "Min",
        "Close",
        "Change",
    ]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("X", "")
            .str.replace("+", "")
            .str.replace("----", "0")
            .str.replace("---", "0")
            .str.replace("--", "0")
        )
    return df


def colname_zh2en(
    df: pd.DataFrame,
    colname: typing.List[str],
) -> pd.DataFrame:
    """資料欄位轉換, 英文有助於接下來存入資料庫"""
    taiwan_stock_price = {
        "證券代號": "StockID",
        "證券名稱": "",
        "成交股數": "TradeVolume",
        "成交筆數": "Transaction",
        "成交金額": "TradeValue",
        "開盤價": "Open",
        "最高價": "Max",
        "最低價": "Min",
        "收盤價": "Close",
        "漲跌(+/-)": "Dir",
        "漲跌價差": "Change",
        "最後揭示買價": "",
        "最後揭示買量": "",
        "最後揭示賣價": "",
        "最後揭示賣量": "",
        "本益比": "",
    }
    df.columns = [
        taiwan_stock_price[col]
        for col in colname
    ]
    df = df.drop([""], axis=1)
    return df


def twse_header():
    """網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request"""
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler_twse(
    date: str,
) -> pd.DataFrame:
    """
    證交所網址
    https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html
    """
    # headers 中的 Request url
    url = (
        "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX"
        "?response=json&date={date}&type=ALL"
    )
    url = url.format(
        date=date.replace("-", "")
    )
    # 避免被證交所 ban ip, 在每次爬蟲時, 先 sleep 5 秒
    time.sleep(5)
    # request method
    res = requests.get(
        url, headers=twse_header()
    )
    if (
        res.json()["stat"]
        == "很抱歉，沒有符合條件的資料!"
    ):
        # 如果 date 是周末，會回傳很抱歉，沒有符合條件的資料!
        return pd.DataFrame()
    df = pd.DataFrame()
    # 證交所資料格式改變，更新程式碼
    try:
        data = res.json()["tables"][8]
        df = pd.DataFrame(data["data"])
        colname = data["fields"]
    except BaseException:
        return pd.DataFrame()

    if len(df) == 0:
        return pd.DataFrame()
    # 欄位中英轉換
    df = colname_zh2en(
        df.copy(), colname
    )
    df["Date"] = date
    return df


class TaiwanStockPrice(BaseModel):
    StockID: str
    TradeVolume: int
    Transaction: int
    TradeValue: int
    Open: float
    Max: float
    Min: float
    Close: float
    Change: float
    Date: str


def check_schema(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """檢查資料型態, 確保每次要上傳資料庫前, 型態正確"""
    df_dict = df.to_dict("records")
    df_schema = [
        TaiwanStockPrice(**dd).__dict__
        for dd in df_dict
    ]
    df = pd.DataFrame(df_schema)
    return df


def gen_date_list(
    start_date: str, end_date: str
) -> typing.List[str]:
    """建立時間列表, 用於爬取所有資料"""
    start_date = (
        datetime.datetime.strptime(
            start_date, "%Y-%m-%d"
        ).date()
    )
    end_date = (
        datetime.datetime.strptime(
            end_date, "%Y-%m-%d"
        ).date()
    )
    days = (
        end_date - start_date
    ).days + 1
    date_list = [
        str(
            start_date
            + datetime.timedelta(
                days=day
            )
        )
        for day in range(days)
    ]
    return date_list


def main(
    start_date: str, end_date: str
):
    """證交所寫明, ※ 本資訊自民國93年2月11日起提供"""
    date_list = gen_date_list(
        start_date, end_date
    )
    db_router = Router()
    for date in tqdm(date_list):
        logger.info(date)
        df = crawler_twse(date=date)
        if len(df) > 0:
            # 資料清理
            df = clear_data(df.copy())
            # 檢查資料型態
            df = check_schema(df.copy())
            # upload db
            try:
                df.to_sql(
                    name="TaiwanStockPrice",
                    con=db_router.mysql_financialdata_conn,
                    if_exists="append",
                    index=False,
                    chunksize=1000,
                )
            except Exception as e:
                logger.info(e)


if __name__ == "__main__":
    start_date, end_date = sys.argv[1:]
    main(start_date, end_date)
