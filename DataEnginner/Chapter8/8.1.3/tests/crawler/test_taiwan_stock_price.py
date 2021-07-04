import pandas as pd

from financialdata.crawler.taiwan_stock_price import (
    clear_data,
    colname_zh2en,
    convert_change,
    convert_date,
    crawler,
    gen_task_paramter_list,
    is_weekend,
    set_column,
)
from financialdata.schema.dataset import check_schema


def test_is_weekend_false():
    result = is_weekend(day=1)
    excepted = False
    assert result == excepted


def test_is_weekend_true():
    result = is_weekend(day=0)
    excepted = True
    assert result == excepted


def test_gen_task_paramter_list():
    result = gen_task_paramter_list(
        start_date="2021-01-01", end_date="2021-01-05"
    )
    excepted = [
        {"date": "2021-01-01", "data_source": "twse"},
        {"date": "2021-01-01", "data_source": "tpex"},
        {"date": "2021-01-02", "data_source": "twse"},
        {"date": "2021-01-02", "data_source": "tpex"},
        {"date": "2021-01-05", "data_source": "twse"},
        {"date": "2021-01-05", "data_source": "tpex"},
    ]
    assert result == excepted


def test_clear_data():
    pass


def test_colname_zh2en():
    result_df = pd.DataFrame(
        [
            {
                0: "0050",
                1: "元大台灣50",
                2: "4,962,514",
                3: "6,179",
                4: "616,480,760",
                5: "124.20",
                6: "124.65",
                7: "123.75",
                8: "124.60",
                9: "<p style= color:red>+</p>",
                10: "0.25",
                11: "124.55",
                12: "123",
                13: "124.60",
                14: "29",
                15: "0.00",
            },
            {
                0: "0051",
                1: "元大中型100",
                2: "175,269",
                3: "44",
                4: "7,827,387",
                5: "44.60",
                6: "44.74",
                7: "44.39",
                8: "44.64",
                9: "<p style= color:red>+</p>",
                10: "0.04",
                11: "44.64",
                12: "20",
                13: "44.74",
                14: "2",
                15: "0.00",
            },
        ]
    )
    colname = [
        "證券代號",
        "證券名稱",
        "成交股數",
        "成交筆數",
        "成交金額",
        "開盤價",
        "最高價",
        "最低價",
        "收盤價",
        "漲跌(+/-)",
        "漲跌價差",
        "最後揭示買價",
        "最後揭示買量",
        "最後揭示賣價",
        "最後揭示賣量",
        "本益比",
    ]
    result_df = colname_zh2en(result_df.copy(), colname)
    excepted_df = pd.DataFrame(
        [
            {
                "StockID": "0050",
                "TradeVolume": "4,962,514",
                "Transaction": "6,179",
                "TradeValue": "616,480,760",
                "Open": "124.20",
                "Max": "124.65",
                "Min": "123.75",
                "Close": "124.60",
                "Dir": "<p style= color:red>+</p>",
                "Change": "0.25",
            },
            {
                "StockID": "0051",
                "TradeVolume": "175,269",
                "Transaction": "44",
                "TradeValue": "7,827,387",
                "Open": "44.60",
                "Max": "44.74",
                "Min": "44.39",
                "Close": "44.64",
                "Dir": "<p style= color:red>+</p>",
                "Change": "0.04",
            },
        ]
    )
    assert pd.testing.assert_frame_equal(result_df, excepted_df) is None


def test_crawler():
    result_df = crawler(
        parameter={"date": "2021-01-05", "data_source": "twse"}
    )
    result_df = check_schema(result_df, "TaiwanStockPrice")
    result_df = result_df[:2]
    excepted_df = pd.DataFrame(
        [
            {
                "StockID": "0050",
                "TradeVolume": 4962514,
                "Transaction": 6179,
                "TradeValue": 616480760,
                "Open": 124.2,
                "Max": 124.65,
                "Min": 123.75,
                "Close": 124.6,
                "Change": 0.25,
                "Date": "2021-01-05",
            },
            {
                "StockID": "0051",
                "TradeVolume": 175269,
                "Transaction": 44,
                "TradeValue": 7827387,
                "Open": 44.6,
                "Max": 44.74,
                "Min": 44.39,
                "Close": 44.64,
                "Change": 0.04,
                "Date": "2021-01-05",
            },
        ]
    )
    assert pd.testing.assert_frame_equal(result_df, excepted_df) is None
