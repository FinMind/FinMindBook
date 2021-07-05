"""
由於書本排版, 
這裡使用 black -l 40 taiwan_stock_price.py
調整程式最大行數,
使用者可再自行調整
"""
import datetime
import time
import typing

import pandas as pd
import requests
from loguru import logger
from financialdata.schema.dataset import (
    check_schema,
)


def is_weekend(day: int) -> bool:
    return day in [0, 6]


def gen_task_paramter_list(start_date: str, end_date: str) -> typing.List[str]:
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    days = (end_date - start_date).days + 1
    date_list = [
        start_date + datetime.timedelta(days=day) for day in range(days)
    ]
    # 排除掉周末非交易日
    date_list = [
        dict(
            date=str(d),
            data_source=data_source,
        )
        for d in date_list
        for data_source in [
            "twse",
            "tpex",
        ]
        if not is_weekend(d.weekday())
    ]
    return date_list


def clear_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """資料清理, 將文字轉成數字"""
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
            .str.replace(" ", "")
            .str.replace("除權息", "0")
            .str.replace("除息", "0")
            .str.replace("除權", "0")
        )
    return df


def colname_zh2en(
    df: pd.DataFrame,
    colname: typing.List[str],
) -> pd.DataFrame:
    """資料欄位轉換, 英文有助於我們接下來存入資料庫"""
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
    df.columns = [taiwan_stock_price[col] for col in colname]
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


def tpex_header():
    """網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request"""
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.tpex.org.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430.php?l=zh-tw",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def set_column(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """設定資料欄位名稱"""
    df.columns = [
        "StockID",
        "Close",
        "Change",
        "Open",
        "Max",
        "Min",
        "TradeVolume",
        "TradeValue",
        "Transaction",
    ]
    return df


def crawler_tpex(
    date: str,
) -> pd.DataFrame:
    """
    櫃買中心網址
    https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430.php?l=zh-tw
    """
    logger.info("crawler_tpex")
    # headers 中的 Request url
    url = "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d={date}&se=AL"
    url = url.format(date=convert_date(date))
    # 避免被櫃買中心 ban ip, 在每次爬蟲時, 先 sleep 5 秒
    time.sleep(5)
    # request method
    res = requests.get(url, headers=tpex_header())
    data = res.json().get("aaData", [])
    df = pd.DataFrame(data)
    if not data or len(df) == 0:
        return pd.DataFrame()
    # 櫃買中心回傳的資料, 並無資料欄位, 因此這裡我們直接用 index 取特定欄位
    df = df[[0, 2, 3, 4, 5, 6, 7, 8, 9]]
    # 欄位中英轉換
    df = set_column(df.copy())
    df["Date"] = date
    df = clear_data(df.copy())
    return df


def crawler_twse(
    date: str,
) -> pd.DataFrame:
    """
    證交所網址
    https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html
    """
    logger.info("crawler_twse")
    # headers 中的 Request url
    url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={date}&type=ALL"
    url = url.format(date=date.replace("-", ""))
    # 避免被證交所 ban ip, 在每次爬蟲時, 先 sleep 5 秒
    time.sleep(5)
    # request method
    res = requests.get(url, headers=twse_header())
    # 2009 年以後的資料, 股價在 response 中的 data9
    # 2009 年以後的資料, 股價在 response 中的 data8
    # 不同格式, 在證交所的資料中, 是很常見的,
    # 沒資料的情境也要考慮進去，例如現在週六沒有交易，但在 2007 年週六是有交易的
    df = pd.DataFrame()
    try:
        if "data9" in res.json():
            df = pd.DataFrame(res.json()["data9"])
            colname = res.json()["fields9"]
        elif "data8" in res.json():
            df = pd.DataFrame(res.json()["data8"])
            colname = res.json()["fields8"]
        elif res.json()["stat"] in [
            "查詢日期小於93年2月11日，請重新查詢!",
            "很抱歉，沒有符合條件的資料!",
        ]:
            pass
    except Exception as e:
        logger.error(e)
        return pd.DataFrame()

    if len(df) == 0:
        return pd.DataFrame()
    # 欄位中英轉換
    df = colname_zh2en(df.copy(), colname)
    df["Date"] = date
    df = convert_change(df.copy())
    df = clear_data(df.copy())
    return df


def convert_change(
    df: pd.DataFrame,
) -> pd.DataFrame:
    logger.info("convert_change")
    df["Dir"] = df["Dir"].str.split(">").str[1].str.split("<").str[0]
    df["Change"] = df["Dir"] + df["Change"]
    df["Change"] = (
        df["Change"].str.replace(" ", "").str.replace("X", "").astype(float)
    )
    df = df.fillna("")
    df = df.drop(["Dir"], axis=1)
    return df


def convert_date(date: str) -> str:
    logger.info("convert_date")
    year, month, day = date.split("-")
    year = int(year) - 1911
    return f"{year}/{month}/{day}"


def crawler(
    parameter: typing.Dict[
        str,
        typing.List[typing.Union[str, int, float]],
    ]
) -> pd.DataFrame:
    logger.info(parameter)
    date = parameter.get("date", "")
    data_source = parameter.get("data_source", "")
    if data_source == "twse":
        df = crawler_twse(date)
    elif data_source == "tpex":
        df = crawler_tpex(date)
    df = check_schema(
        df.copy(),
        dataset="TaiwanStockPrice",
    )
    return df
