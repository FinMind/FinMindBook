from airflow.operators.python_operator import (
    PythonOperator,
)


def create_python_operator_task() -> PythonOperator:
    return PythonOperator(
        task_id="PythonOperator",
        python_callable=lambda: print(
            "PythonOperator"
        ),
    )
