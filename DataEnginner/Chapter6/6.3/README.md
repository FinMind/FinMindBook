# FinMindBook
FinMind Book

## run
    pipenv run uvicorn main:app --reload --port 8888

## 壓測
    ab -c 1 -n 10  'http://127.0.0.1:8000/'
