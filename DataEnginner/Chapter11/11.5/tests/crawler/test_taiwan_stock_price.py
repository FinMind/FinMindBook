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
    twse_header,
    tpex_header,
    crawler_twse,
    crawler_tpex,
)
from financialdata.schema.dataset import (
    check_schema,
)


def test_is_weekend_false():
    """
    測試, 非周末, 輸入周一 1, 回傳 False
    """
    result = is_weekend(day=1)  # 執行結果
    expected = False
    # 先寫好預期結果, 這樣即使不執行程式,
    # 單純看測試, 也能了解這個程式的執行結果
    assert (
        result == expected
    )  # 檢查, 執行結果 == 預期結果


def test_is_weekend_true():
    """
    測試, 是周末, 輸入週日 0, 回傳 False
    """
    result = is_weekend(day=0)  # 執行結果
    expected = True
    # 先寫好預期結果, 這樣即使不執行程式,
    # 單純看測試, 也能了解這個程式的執行結果
    assert (
        result == expected
    )  # 檢查, 執行結果 == 預期結果


def test_gen_task_paramter_list():
    """
    測試建立 task 參數列表, 2021-01-01 ~ 2021-01-05
    """
    result = gen_task_paramter_list(
        start_date="2021-01-01",
        end_date="2021-01-05",
    )  # 執行結果
    expected = [
        {
            "date": "2021-01-01",
            "data_source": "twse",
        },
        {
            "date": "2021-01-01",
            "data_source": "tpex",
        },
        {
            "date": "2021-01-02",
            "data_source": "twse",
        },
        {
            "date": "2021-01-02",
            "data_source": "tpex",
        },
        {
            "date": "2021-01-05",
            "data_source": "twse",
        },
        {
            "date": "2021-01-05",
            "data_source": "tpex",
        },
    ]
    # 預期得到 2021-01-01 ~ 2021-01-05 的任務參數列表
    # 再發送這些參數到 rabbitmq, 給每個 worker 單獨執行爬蟲
    assert (
        result == expected
    )  # 檢查, 執行結果 == 預期結果


def test_clear_data():
    #  準備好 input 的假資料
    df = pd.DataFrame(
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
                "Change": 0.25,
                "Date": "2021-01-05",
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
                "Change": 0.04,
                "Date": "2021-01-05",
            },
            {
                "StockID": "0052",
                "TradeVolume": "1,536,598",
                "Transaction": "673",
                "TradeValue": "172,232,526",
                "Open": "112.10",
                "Max": "112.90",
                "Min": "111.15",
                "Close": "112.90",
                "Change": 0.8,
                "Date": "2021-01-05",
            },
        ]
    )
    result_df = clear_data(
        df.copy()
    )  # 輸入函數, 得到結果
    expected_df = pd.DataFrame(
        [
            {
                "StockID": "0050",
                "TradeVolume": "4962514",
                "Transaction": "6179",
                "TradeValue": "616480760",
                "Open": "124.20",
                "Max": "124.65",
                "Min": "123.75",
                "Close": "124.60",
                "Change": "0.25",
                "Date": "2021-01-05",
            },
            {
                "StockID": "0051",
                "TradeVolume": "175269",
                "Transaction": "44",
                "TradeValue": "7827387",
                "Open": "44.60",
                "Max": "44.74",
                "Min": "44.39",
                "Close": "44.64",
                "Change": "0.04",
                "Date": "2021-01-05",
            },
            {
                "StockID": "0052",
                "TradeVolume": "1536598",
                "Transaction": "673",
                "TradeValue": "172232526",
                "Open": "112.10",
                "Max": "112.90",
                "Min": "111.15",
                "Close": "112.90",
                "Change": "0.8",
                "Date": "2021-01-05",
            },
        ]
    )
    # 預期結果, 做完資料清理
    # 將原先的會計數字, 如 1,536,598
    # 轉換為一般數字 1536598
    assert (
        pd.testing.assert_frame_equal(
            result_df, expected_df
        )
        is None
    )  # 檢查, 執行結果 == 預期結果


def test_colname_zh2en():
    #  準備好 input 的假資料
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
    result_df = colname_zh2en(
        result_df.copy(), colname
    )  # 輸入函數, 得到結果
    expected_df = pd.DataFrame(
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
    # 預期結果, 將 raw data , 包含中文欄位,
    # 轉換成英文欄位, 以便存進資料庫
    assert (
        pd.testing.assert_frame_equal(
            result_df, expected_df
        )
        is None
    )  # 檢查, 執行結果 == 預期結果


def test_twse_header():
    result = twse_header()
    expected = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    assert result == expected


def test_tpex_header():
    result = tpex_header()
    expected = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.tpex.org.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430.php?l=zh-tw",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    assert result == expected


def test_set_column():
    #  準備好 input 的假資料
    df = pd.DataFrame(
        [
            {
                0: "00679B",
                2: "44.91",
                3: "-0.08",
                4: "45.00",
                5: "45.00",
                6: "44.85",
                7: "270,000",
                8: "12,127,770",
                9: "147",
            },
            {
                0: "00687B",
                2: "47.03",
                3: "-0.09",
                4: "47.13",
                5: "47.13",
                6: "47.00",
                7: "429,000",
                8: "20,181,570",
                9: "39",
            },
            {
                0: "00694B",
                2: "37.77",
                3: "-0.07",
                4: "37.84",
                5: "37.84",
                6: "37.72",
                7: "343,000",
                8: "12,943,630",
                9: "35",
            },
        ]
    )
    result_df = set_column(
        df
    )  # 輸入函數, 得到結果
    expected_df = pd.DataFrame(
        [
            {
                "StockID": "00679B",
                "Close": "44.91",
                "Change": "-0.08",
                "Open": "45.00",
                "Max": "45.00",
                "Min": "44.85",
                "TradeVolume": "270,000",
                "TradeValue": "12,127,770",
                "Transaction": "147",
            },
            {
                "StockID": "00687B",
                "Close": "47.03",
                "Change": "-0.09",
                "Open": "47.13",
                "Max": "47.13",
                "Min": "47.00",
                "TradeVolume": "429,000",
                "TradeValue": "20,181,570",
                "Transaction": "39",
            },
            {
                "StockID": "00694B",
                "Close": "37.77",
                "Change": "-0.07",
                "Open": "37.84",
                "Max": "37.84",
                "Min": "37.72",
                "TradeVolume": "343,000",
                "TradeValue": "12,943,630",
                "Transaction": "35",
            },
        ]
    )
    # 預期結果, 根據資料的位置, 設置對應的欄位名稱
    assert (
        pd.testing.assert_frame_equal(
            result_df, expected_df
        )
        is None
    )  # 檢查, 執行結果 == 預期結果


def test_crawler_twse_data9():
    """
    測試在證交所, 2021 正常爬到資料的情境,
    data 在 response 底下的 key, data9
    一般政府網站, 長時間的資料, 格式常常不一致
    """
    result_df = crawler_twse(
        date="2021-01-05"
    )  # 執行結果
    assert (
        len(result_df) == 20596
    )  # 檢查, 資料量是否正確
    assert list(result_df.columns) == [
        "StockID",
        "TradeVolume",
        "Transaction",
        "TradeValue",
        "Open",
        "Max",
        "Min",
        "Close",
        "Change",
        "Date",
    ]  # 檢查, 資料欄位是否正確


def test_crawler_twse_data8():
    """
    測試在證交所, 2008 正常爬到資料的情境, 時間不同, 資料格式不同
    data 在 response 底下的 key, data8
    一般政府網站, 長時間的資料, 格式常常不一致
    """
    result_df = crawler_twse(
        date="2008-01-04"
    )
    assert (
        len(result_df) == 2760
    )  # 檢查, 資料量是否正確
    assert list(result_df.columns) == [
        "StockID",
        "TradeVolume",
        "Transaction",
        "TradeValue",
        "Open",
        "Max",
        "Min",
        "Close",
        "Change",
        "Date",
    ]  # 檢查, 資料欄位是否正確


def test_crawler_twse_no_data():
    """
    測試沒 data 的時間點, 爬蟲是否正常
    """
    result_df = crawler_twse(
        date="2000-01-04"
    )
    assert (
        len(result_df) == 0
    )  # 沒 data, 回傳 0
    # 沒 data, 一樣要回傳 pd.DataFrame 型態
    assert isinstance(
        result_df, pd.DataFrame
    )


def test_crawler_twse_error(mocker):
    """
    測試對方網站回傳例外狀況時, 或是被 ban IP 時, 爬蟲是否會失敗

    這邊使用特別的技巧, mocker,
    因為在測試階段, 我們無法保證對方一定會給錯誤的結果
    因此使用 mocker, 對 requests 做"替換", 換成我們設定的結果
    如下
    """
    # 將特定路徑下的 requests 替換掉
    mock_requests = mocker.patch(
        "financialdata.crawler.taiwan_stock_price.requests"
    )
    # 將 requests.get 的回傳值 response, 替換掉成 ""
    # 如此一來, 當我們在測試爬蟲時,
    # 發送 requests 得到的 response, 就會是 ""
    mock_requests.get.return_value = ""
    result_df = crawler_twse(
        date="2000-01-04"
    )
    assert (
        len(result_df) == 0
    )  # 沒 data, 回傳 0
    # 沒 data, 一樣要回傳 pd.DataFrame 型態
    assert isinstance(
        result_df, pd.DataFrame
    )


def test_crawler_tpex_success():
    """
    測試櫃買中心, 爬蟲成功時的狀況
    """
    result_df = crawler_tpex(
        date="2021-01-05"
    )  # 執行結果
    assert (
        len(result_df) == 6609
    )  # 檢查, 資料量是否正確
    assert list(result_df.columns) == [
        "StockID",
        "Close",
        "Change",
        "Open",
        "Max",
        "Min",
        "TradeVolume",
        "TradeValue",
        "Transaction",
        "Date",
    ]


def test_crawler_tpex_no_data():
    """
    測試沒 data 的時間點, 爬蟲是否正常
    """
    result_df = crawler_tpex(
        date="2021-01-01"
    )
    assert (
        len(result_df) == 0
    )  # 沒 data, 回傳 0
    # 沒 data, 一樣要回傳 pd.DataFrame 型態
    assert isinstance(
        result_df, pd.DataFrame
    )


def test_convert_change():
    #  準備好 input 的假資料
    df = pd.DataFrame(
        [
            {
                "StockID": "0050",
                "TradeVolume": "4,680,733",
                "Transaction": "5,327",
                "TradeValue": "649,025,587",
                "Open": "139.00",
                "Max": "139.20",
                "Min": "138.05",
                "Close": "138.30",
                "Dir": "<p style= color:green>-</p>",
                "Change": "0.65",
                "Date": "2021-07-01",
            },
            {
                "StockID": "0051",
                "TradeVolume": "175,374",
                "Transaction": "120",
                "TradeValue": "10,152,802",
                "Open": "58.20",
                "Max": "59.10",
                "Min": "57.40",
                "Close": "57.90",
                "Dir": "<p style= color:green>-</p>",
                "Change": "0.30",
                "Date": "2021-07-01",
            },
            {
                "StockID": "0052",
                "TradeVolume": "514,042",
                "Transaction": "270",
                "TradeValue": "64,127,738",
                "Open": "125.00",
                "Max": "125.20",
                "Min": "124.35",
                "Close": "124.35",
                "Dir": "<p style= color:green>-</p>",
                "Change": "0.65",
                "Date": "2021-07-01",
            },
        ]
    )
    result_df = convert_change(
        df
    )  # 執行結果
    expected_df = pd.DataFrame(
        [
            {
                "StockID": "0050",
                "TradeVolume": "4,680,733",
                "Transaction": "5,327",
                "TradeValue": "649,025,587",
                "Open": "139.00",
                "Max": "139.20",
                "Min": "138.05",
                "Close": "138.30",
                "Change": -0.65,
                "Date": "2021-07-01",
            },
            {
                "StockID": "0051",
                "TradeVolume": "175,374",
                "Transaction": "120",
                "TradeValue": "10,152,802",
                "Open": "58.20",
                "Max": "59.10",
                "Min": "57.40",
                "Close": "57.90",
                "Change": -0.3,
                "Date": "2021-07-01",
            },
            {
                "StockID": "0052",
                "TradeVolume": "514,042",
                "Transaction": "270",
                "TradeValue": "64,127,738",
                "Open": "125.00",
                "Max": "125.20",
                "Min": "124.35",
                "Close": "124.35",
                "Change": -0.65,
                "Date": "2021-07-01",
            },
        ]
    )
    # 預期結果,
    # 將 Dir (正負號) 與 Change (漲跌幅) 結合
    assert (
        pd.testing.assert_frame_equal(
            result_df, expected_df
        )
        is None
    )  # 檢查, 執行結果 == 預期結果


def test_convert_date():
    date = (
        "2021-07-01"  #  準備好 input 的假資料
    )
    result = convert_date(date)  # 執行結果
    expected = "110/07/01"  # 預期結果
    assert (
        result == expected
    )  # 檢查, 執行結果 == 預期結果


def test_crawler_twse():
    # 測試證交所爬蟲, end to end test
    result_df = crawler(
        parameter={
            "date": "2021-01-05",
            "data_source": "twse",
        }
    )
    result_df = check_schema(
        result_df, "TaiwanStockPrice"
    )
    assert len(result_df) > 0


def test_crawler_tpex():
    # 測試櫃買中心爬蟲, end to end test
    result_df = crawler(
        parameter={
            "date": "2021-01-05",
            "data_source": "tpex",
        }
    )
    result_df = check_schema(
        result_df, "TaiwanStockPrice"
    )
    assert len(result_df) > 0
