import time
from multiprocessing import Process

import pytest
import requests
import uvicorn
from fastapi.testclient import (
    TestClient,
)
from sqlalchemy import engine

from api.main import (
    app,
    get_mysql_financialdata_conn,
)

client = TestClient(app)
# 使用 fastapi 官方教學
# https://fastapi.tiangolo.com/tutorial/testing/
# 測試框架

# 測試對資料庫的連線,
# assert 回傳的物件, 是一個 sqlalchemy 的 connect 物件
def test_get_mysql_financialdata_conn():
    conn = (
        get_mysql_financialdata_conn()
    )
    assert isinstance(
        conn, engine.Connection
    )


# 測試對 'http://127.0.0.1:5000/' 頁面發送 request,
# 得到的回應 response 的狀態 status_code, json data
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Hello": "World"
    }


# 測試對 'http://127.0.0.1:5000/taiwan_stock_price' 頁面發送 request,
# 並帶 stock_id, start_date, end_date 參數
# 得到的回應 response 的狀態 status_code, json data
def test_taiwan_stock_price():
    response = client.get(
        "/taiwan_stock_price",
        params=dict(
            stock_id="2330",
            start_date="2021-04-01",
            end_date="2021-04-01",
        ),
    )
    assert response.status_code == 200
    # 以下特別重要, 需要把 response 結果寫死
    # 避免未來 api schema 改變時, 影響 api 的使用者
    # 例如 Open 目前 response 是 float, 598.0,
    # 未來就不能改成 int, 598, 這是不被允許的
    # 因為 float -> int, 會大大影響使用者進行資料處理
    # 同理, int -> float 也是禁止的,
    # 資料型態在一開始就必須決定好
    assert response.json() == {
        "data": [
            {
                "StockID": "2330",
                "TradeVolume": 45972766,
                "Transaction": 48170,
                "TradeValue": 27520742963,
                "Open": 598.0,
                "Max": 602.0,
                "Min": 594.0,
                "Close": 602.0,
                "Change": 15.0,
                "Date": "2021-04-01",
            }
        ]
    }


# end to end 測試, 模擬真實使用 request 套件發送請求
# 使用 Process 開另一個進程, 模擬啟動 api
# 之後會在主進程, 對此 api 發送 request
@pytest.fixture(scope="module")
def setUp():
    proc = Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={
            "host": "127.0.0.1",
            "port": 5000,
            "log_level": "info",
        },
        daemon=True,
    )
    proc.start()
    time.sleep(1)
    return 1


# 測試對 api 發送 requests,
# assert 回傳結果是 {"Hello": "World"}
def test_index(setUp):
    response = requests.get(
        "http://127.0.0.1:5000"
    )
    assert response.json() == {
        "Hello": "World"
    }


# 測試對 api 發送 requests,
# assert 回傳的 data, 這裡把真實的 case 寫下來
# 跟 test_taiwan_stock_price 概念一樣,
# 唯一的差別是, 這裡是真實場景, 對 api 發送 requests
def test_TaiwanStockPriceID(setUp):
    payload = {
        "stock_id": "2330",
        "start_date": "2021-04-01",
        "end_date": "2021-04-01",
    }
    res = requests.get(
        "http://127.0.0.1:5000/taiwan_stock_price",
        params=payload,
    )
    resp = res.json()["data"]
    assert resp == [
        {
            "StockID": "2330",
            "TradeVolume": 45972766,
            "Transaction": 48170,
            "TradeValue": 27520742963,
            "Open": 598.0,
            "Max": 602.0,
            "Min": 594.0,
            "Close": 602.0,
            "Change": 15.0,
            "Date": "2021-04-01",
        }
    ]
