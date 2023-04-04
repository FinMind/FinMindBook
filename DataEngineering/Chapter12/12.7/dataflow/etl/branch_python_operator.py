from airflow.operators.dummy_operator import (
    DummyOperator,
)
from airflow.operators.python_operator import (
    BranchPythonOperator,
    PythonOperator,
)


def create_skip_task() -> DummyOperator:
    return DummyOperator(task_id="skip")


def create_crawler_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler",
        python_callable=lambda: print(
            "crawler"
        ),
    )


def check_crawler():
    # 檢查今天是否以爬蟲
    # 如果已經爬蟲了，則跳過
    if True:
        return "skip"
    else:
        return "crawler"


def create_branch_python_operator_task():
    check_crawler_task = BranchPythonOperator(
        task_id="CheckCrawler",
        python_callable=check_crawler,
    )
    skip_task = create_skip_task()
    crawler_task = create_crawler_task()
    return check_crawler_task >> [
        skip_task,
        crawler_task,
    ]
