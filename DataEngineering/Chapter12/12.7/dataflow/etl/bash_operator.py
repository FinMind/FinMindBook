from airflow.operators.bash_operator import (
    BashOperator,
)


def create_bash_operator_task() -> BashOperator:
    return BashOperator(
        task_id="BashOperator",
        bash_command="echo BashOperator",
    )
