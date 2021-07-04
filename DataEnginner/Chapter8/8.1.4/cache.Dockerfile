FROM finminddocker/finmind_crawler:latest

COPY ./financialdata /FinMindProject/financialdata
COPY .env /FinMindProject

WORKDIR /FinMindProject/