from pydantic import BaseModel


import pandas as pd


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
    date: str


class TaiwanFuturesDaily(BaseModel):
    date: str
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


def check_schema(df: pd.DataFrame) -> pd.DataFrame:
    """ 檢查資料型態, 確保每次要上傳資料庫前, 型態正確 """
    df_dict = df.to_dict("r")
    df_schema = [TaiwanFuturesDaily(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df



