from pydantic import BaseModel
import importlib

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
    Date: str


def check_schema(
    df: pd.DataFrame, dataset: str
) -> pd.DataFrame:
    """檢查資料型態, 確保每次要上傳資料庫前, 型態正確"""
    df_dict = df.to_dict("records")
    schema = getattr(
        importlib.import_module(
            "dataflow.schema.dataset"
        ),
        dataset,
    )
    df_schema = [
        schema(**dd).__dict__
        for dd in df_dict
    ]
    df = pd.DataFrame(df_schema)
    return df
