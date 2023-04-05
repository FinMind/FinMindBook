from airflow.operators.python_operator import (
    PythonOperator,
)


def create_hello_world_task() -> PythonOperator:
    return PythonOperator(
        task_id="hello_world",
        python_callable=lambda: print(
            "hello_world"
        ),
    )
