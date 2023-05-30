import airflow

from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)
from dataflow.etl.python_operator import (
    create_python_operator_task,
)

with airflow.DAG(
    dag_id="PythonOperator",
    default_args=DEFAULT_ARGS,
    schedule_interval="*/5 * * * *",
    max_active_runs=MAX_ACTIVE_RUNS,
    catchup=False,
) as dag:
    create_python_operator_task()
