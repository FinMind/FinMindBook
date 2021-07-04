from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price():
    print("get data from mysql")
    return {"data": 123}
