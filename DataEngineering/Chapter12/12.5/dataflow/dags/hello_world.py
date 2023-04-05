import airflow

from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)
from dataflow.etl.hello_world import (
    create_hello_world_task,
)

with airflow.DAG(
    dag_id="HelloWorld",
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    max_active_runs=MAX_ACTIVE_RUNS,
    catchup=False,
) as dag:
    create_hello_world_task()
