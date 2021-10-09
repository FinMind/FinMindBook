"""
由於書本排版, 
這裡使用 black -l 40 taiwan_stock_price.py
調整程式最大行數,
使用者可再自行調整
"""
import datetime
import typing
from lxml import etree
import pandas as pd
from loguru import logger
from financialdata.utility import (
    request,
)
from financialdata.utility.common import (
    get_today,
)
from financialdata.schema.dataset import (
    check_schema,
)


def no_crawler_list():
    # 不抓權證類股票
    return [
        "全部",
        "全部(不含權證、牛熊證、可展延牛熊證)",
        "所有證券(不含權證、牛熊證)",
        "封閉式基金",
        "受益證券",
        "認購售權證",
        "展延型牛熊證",
        "認購權證(不含牛證)",
        "認售權證(不含熊證)",
        "牛證(不含可展延牛證)",
        "熊證(不含可展延熊證)",
        "牛熊證(不含展延型牛熊證)",
        "可展延牛證",
        "可展延熊證",
        "附認股權特別股",
        "附認股權公司債",
        "可轉換公司債",
        "認股權憑證",
        "所有證券",
        "委託及成交資訊(16:05提供)",
    ]


def twse_header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Pragma": "no-cache",
        "Referer": "http://www.twse.com.tw/zh/page/trading/exchange/FMSRFK.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    }


def tpex_header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.tpex.org.tw",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    }


def gen_twse_task_paramter_list() -> typing.List[
    typing.Dict[
        str,
        typing.Union[str, int, float],
    ]
]:
    url = "http://www.twse.com.tw/zh/page/trading/exchange/BFT41U.html"
    res = request.get(
        url, twse_header(), sleep=5
    )
    res.encoding = "utf-8"
    page = etree.HTML(res.text)
    temp = page.xpath("//option")
    loop_list = [
        dict(
            id=te.attrib["value"],
            industry_category=te.text,
            data_source="twse",
        )
        for te in temp
        if te.text.replace(" ", "")
        not in no_crawler_list()
    ]
    return loop_list


def gen_tpex_task_paramter_list() -> typing.List[
    typing.Dict[
        str,
        typing.Union[str, int, float],
    ]
]:
    url = "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430.php?l=zh-tw"
    res = request.get(
        url, tpex_header(), sleep=5
    )
    res.encoding = "utf-8"
    page = etree.HTML(res.text)
    temp = page.xpath("//option")
    loop_list = [
        dict(
            id=te.attrib["value"],
            industry_category=te.text,
            data_source="tpex",
        )
        for te in temp
        if te.text.replace(" ", "")
        not in no_crawler_list()
    ]
    return loop_list


def gen_task_paramter_list(
    **kwargs,
) -> typing.List[
    typing.Dict[
        str,
        typing.Union[str, int, float],
    ]
]:
    task_paramter_list = []
    [
        task_paramter_list.extend(
            task_list
        )
        for task_list in [
            gen_twse_task_paramter_list(),
            gen_tpex_task_paramter_list(),
        ]
    ]
    return task_paramter_list


def crawler_twse(
    _id: str, industry_category: str
) -> pd.DataFrame:
    url = f"https://www.twse.com.tw/zh/api/codeFilters?filter={_id}"
    res = request.get(
        url, twse_header(), sleep=5
    )
    df = pd.DataFrame(res.json())
    if len(df) == 0:
        return pd.DataFrame()
    df["stock_id"] = (
        df["resualt"]
        .str.split("\t")
        .str[0]
    )
    df["stock_name"] = (
        df["resualt"]
        .str.split("\t")
        .str[1]
    )
    df = df.drop(
        ["resualt", "filter"], axis=1
    )
    df[
        "industry_category"
    ] = industry_category
    df["type"] = "twse"
    df["date"] = get_today()
    df = df[df["stock_name"] != "合計"]
    return df


def crawler_tpex(
    _id: str, industry_category: str
) -> pd.DataFrame:
    today = get_today(
        string=False
    ) - datetime.timedelta(3)
    old_year = str(today.year)
    new_year = str(today.year - 1911)
    for i in range(5):
        if today.weekday() in [5, 6]:
            today -= datetime.timedelta(
                1
            )
        else:
            today = (
                str(today)
                .replace(
                    old_year, new_year
                )
                .replace("-", "/")
            )
            break
    url = f"https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d={today}&se={_id}"
    res = request.get(
        url, tpex_header(), sleep=5
    )
    tem = res.json()
    df = pd.DataFrame(tem["aaData"])
    if len(df) == 0:
        return pd.DataFrame()
    df = df[[0, 1]]
    df.columns = [
        "stock_id",
        "stock_name",
    ]
    df[
        "industry_category"
    ] = industry_category
    df["type"] = "tpex"
    df["date"] = get_today()
    df = df[df["stock_name"] != "合計"]
    return df


def crawler(
    parameter: typing.Dict[str, str],
    **kwargs,
) -> pd.DataFrame:
    logger.info(parameter)
    _id = parameter.get("id")
    industry_category = parameter.get(
        "industry_category"
    )
    data_source = parameter.get("data_source")
    if data_source == "twse":
        df = crawler_twse(
            _id, industry_category
        )
    elif data_source == "tpex":
        df = crawler_tpex(
            _id, industry_category
        )
    return df
