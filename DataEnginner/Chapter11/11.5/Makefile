
# 建立 network
create-network:
	docker network create my_network

# 建立 mysql volume
create-mysql-volume:
	docker volume create mysql

# 啟動 mysql
create-mysql:
	docker-compose -f mysql.yml up -d

# 啟動 rabbitmq
create-rabbitmq:
	docker-compose -f rabbitmq.yml up -d

# 安裝環境
install-python-env:
	pipenv sync

# 啟動 celery, 專門執行 twse queue 列隊的任務，
run-celery-twse:
	pipenv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q twse

# 啟動 celery, 專門執行 tpex queue 列隊的任務，
run-celery-tpex:
	pipenv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q tpex

# sent task
sent-taiwan-stock-price-task:
	pipenv run python financialdata/producer.py taiwan_stock_price 2021-04-01 2021-04-12

# 建立 dev 環境變數
gen-dev-env-variable:
	python genenv.py

# 建立 staging 環境變數
gen-staging-env-variable:
	VERSION=STAGING python genenv.py

# 建立 release 環境變數
gen-release-env-variable:
	VERSION=RELEASE python genenv.py

build-image:
	docker build -f Dockerfile -t crawler:11.5 .

up-crawler:
	docker-compose -f crawler.yml up

up-multi-crawler:
	docker-compose -f crawler_multi_celery.yml up

up-scheduler:
	docker-compose -f scheduler.yml up

tag-image:
	docker tag crawler:11.5 linsamtw/crawler:11.5

push-image:
	docker push linsamtw/crawler:11.5

run-scheduler:
	pipenv run python financialdata/scheduler.py

test-cov:
	pipenv run pytest --cov-report term-missing --cov-config=.coveragerc --cov=./financialdata/ tests/

# format
format:
	black -l 40 financialdata tests