from airflow.operators.email_operator import (
    EmailOperator,
)


def create_email_operator_task() -> EmailOperator:
    return EmailOperator(
        task_id="EmailOperator",
        to="samlin266118@gmail.com",
        subject="Airflow",
        html_content="Hello, World!",
    )
