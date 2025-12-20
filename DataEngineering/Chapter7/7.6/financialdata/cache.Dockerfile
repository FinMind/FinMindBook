FROM linsamtw/crawler3:latest

COPY ./financialdata /FinMindProject/financialdata
COPY .env /FinMindProject

WORKDIR /FinMindProject/