# FinMindBook
FinMind Book

## run
    pipenv run uvicorn main:app --reload --port 8888

## 壓測
    ab -c 10 -n 1000  'http://127.0.0.1:8888/'
