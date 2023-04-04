from airflow.operators.dummy_operator import (
    DummyOperator,
)


def create_dummy_operator_task() -> DummyOperator:
    return DummyOperator(
        task_id="DummyOperator"
    )
