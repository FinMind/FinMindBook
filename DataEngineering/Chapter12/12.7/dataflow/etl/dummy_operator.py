from airflow.operators.python_operator import (
    PythonOperator,
)


def create_crawler1_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler1",
        python_callable=lambda: print(
            "crawler1"
        ),
    )


def create_crawler2_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler2",
        python_callable=lambda: print(
            "crawler2"
        ),
    )


def create_crawler3_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler3",
        python_callable=lambda: print(
            "crawler3"
        ),
    )


def create_stock_strategy_task() -> PythonOperator:
    return PythonOperator(
        task_id="stock_strategy",
        python_callable=lambda: print(
            "stock_strategy"
        ),
    )
