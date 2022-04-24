FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# install package
RUN pip install pipenv==2020.6.2 && pipenv sync

# genenv
RUN VERSION=RELEASE python genenv.py
 
# 預設執行的指令
CMD ["pipenv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
