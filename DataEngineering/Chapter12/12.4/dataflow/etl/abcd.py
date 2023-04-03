from airflow.operators.python_operator import (
    PythonOperator,
)


def create_a_task() -> PythonOperator:
    return PythonOperator(
        task_id="a",
        python_callable=lambda: print(
            "a"
        ),
    )


def create_b_task() -> PythonOperator:
    return PythonOperator(
        task_id="b",
        python_callable=lambda: print(
            "b"
        ),
    )


def create_c_task() -> PythonOperator:
    return PythonOperator(
        task_id="c",
        python_callable=lambda: print(
            "c"
        ),
    )


def create_d_task() -> PythonOperator:
    return PythonOperator(
        task_id="d",
        python_callable=lambda: print(
            "d"
        ),
    )
