import requests
import pandas as pd

payload = dict(
    stock_id="2330",
    start_date="2021-04-01",
    end_date="2021-04-15",
)
res = requests.get("http://127.0.0.1:8888/taiwan_stock_price", params=payload)
df = pd.DataFrame(res.json()['data'])
df
