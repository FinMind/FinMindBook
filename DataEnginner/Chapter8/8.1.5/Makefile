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
	docker build -f Dockerfile -t api:7.2.2 .

up-api:
	docker-compose -f api.yml up

tag-image:
	docker tag api:7.2.2 linsamtw/api:7.2.2

push-image:
	docker push linsamtw/api:7.2.2

test-cov:
	pipenv run pytest --cov-report term-missing --cov-config=.coveragerc --cov=./api/ tests/

format:
	black -l 80 api tests
