FROM linsamtw/crawler:latest

RUN VERSION=RELEASE python genenv.py
COPY ./financialdata /FinMindProject/financialdata

WORKDIR /FinMindProject/