FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# install package
RUN pip install pipenv && \
    pipenv sync

# genenv
RUN VERSION=DEPLOY python genenv.py

CMD ["/bin/bash"]