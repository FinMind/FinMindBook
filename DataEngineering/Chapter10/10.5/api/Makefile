# 安裝環境
install-python-env:
	pipenv sync

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
	docker build -f Dockerfile -t linsamtw/api:10 .

up-api:
	docker-compose -f api.yml up

push-image:
	docker push linsamtw/api:10

test-cov:
	pipenv run pytest --cov-report term-missing --cov-config=.coveragerc --cov=./api/ tests/

format:
	black -l 40 api tests

deploy:
	docker stack deploy -c api.yml api
