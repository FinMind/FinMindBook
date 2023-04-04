import airflow

from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)
from dataflow.etl.email_operator import (
    create_email_operator_task,
)

with airflow.DAG(
    dag_id="EmailOperator",
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    max_active_runs=MAX_ACTIVE_RUNS,
    catchup=False,
) as dag:
    create_email_operator_task()
