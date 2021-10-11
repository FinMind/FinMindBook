import datetime
import io
import sys
import time
import typing

import pandas as pd
import requests
from loguru import logger
from pydantic import BaseModel
from tqdm import tqdm

from financialdata.router import Router


def futures_header():
    """網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request"""
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "101",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.taifex.com.tw",
        "Origin": "https://www.taifex.com.tw",
        "Pragma": "no-cache",
        "Referer": "https://www.taifex.com.tw/cht/3/dlFutDailyMarketView",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    }


def colname_zh2en(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """資料欄位轉換, 英文有助接下來存入資料庫"""
    colname_dict = {
        "交易日期": "Date",
        "契約": "FuturesID",
        "到期月份(週別)": "ContractDate",
        "開盤價": "Open",
        "最高價": "Max",
        "最低價": "Min",
        "收盤價": "Close",
        "漲跌價": "Change",
        "漲跌%": "ChangePer",
        "成交量": "Volume",
        "結算價": "SettlementPrice",
        "未沖銷契約數": "OpenInterest",
        "交易時段": "TradingSession",
    }
    df = df.drop(
        [
            "最後最佳買價",
            "最後最佳賣價",
            "歷史最高價",
            "歷史最低價",
            "是否因訊息面暫停交易",
            "價差對單式委託成交量",
        ],
        axis=1,
    )
    df.columns = [
        colname_dict[col]
        for col in df.columns
    ]
    return df


def clean_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """資料清理"""
    df["Date"] = df["Date"].str.replace(
        "/", "-"
    )
    df["ChangePer"] = df[
        "ChangePer"
    ].str.replace("%", "")
    df["ContractDate"] = (
        df["ContractDate"]
        .astype(str)
        .str.replace(" ", "")
    )
    if "TradingSession" in df.columns:
        df["TradingSession"] = df[
            "TradingSession"
        ].map(
            {
                "一般": "Position",
                "盤後": "AfterMarket",
            }
        )
    else:
        df[
            "TradingSession"
        ] = "Position"
    for col in [
        "Open",
        "Max",
        "Min",
        "Close",
        "Change",
        "ChangePer",
        "Volume",
        "SettlementPrice",
        "OpenInterest",
    ]:
        df[col] = (
            df[col]
            .replace("-", "0")
            .astype(float)
        )
    df = df.fillna(0)
    return df


def crawler_futures(
    date: str,
) -> pd.DataFrame:
    """期交所爬蟲"""
    url = "https://www.taifex.com.tw/cht/3/futDataDown"
    form_data = {
        "down_type": "1",
        "commodity_id": "all",
        "queryStartDate": date.replace(
            "-", "/"
        ),
        "queryEndDate": date.replace(
            "-", "/"
        ),
    }
    # 避免被期交所 ban ip, 在每次爬蟲時, 先 sleep 5 秒
    time.sleep(5)
    resp = requests.post(
        url,
        headers=futures_header(),
        data=form_data,
    )
    if resp.ok:
        if resp.content:
            df = pd.read_csv(
                io.StringIO(
                    resp.content.decode(
                        "big5"
                    )
                ),
                index_col=False,
            )
    else:
        return pd.DataFrame()
    return df


class TaiwanFuturesDaily(BaseModel):
    Date: str
    FuturesID: str
    ContractDate: str
    Open: float
    Max: float
    Min: float
    Close: float
    Change: float
    ChangePer: float
    Volume: float
    SettlementPrice: float
    OpenInterest: int
    TradingSession: str


def check_schema(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """檢查資料型態, 確保每次要上傳資料庫前, 型態正確"""
    df_dict = df.to_dict("records")
    df_schema = [
        TaiwanFuturesDaily(
            **dd
        ).__dict__
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
    date_list = gen_date_list(
        start_date, end_date
    )
    db_router = Router()
    for date in tqdm(date_list):
        logger.info(date)
        df = crawler_futures(date)
        if len(df) > 0:
            # 欄位中英轉換
            df = colname_zh2en(
                df.copy()
            )
            # 資料清理
            df = clean_data(df.copy())
            # 檢查資料型態
            df = check_schema(df.copy())
            # upload db
            try:
                df.to_sql(
                    name="TaiwanFutures",
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
