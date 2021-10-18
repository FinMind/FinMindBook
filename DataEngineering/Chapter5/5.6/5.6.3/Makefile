
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

# run scheduler
run-scheduler:
	pipenv run python scheduler.py
	