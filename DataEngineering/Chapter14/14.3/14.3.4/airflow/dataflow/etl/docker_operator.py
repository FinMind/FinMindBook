from airflow.operators.docker_operator import (
    DockerOperator,
)


def create_docker_operator_task() -> (
    DockerOperator
):
    return DockerOperator(
        task_id="DockerOperator",
        image="linsamtw/dataflow3:12.7",
        command="uv run --env-file=.env python dataflow/crawler.py",
        # 每次執行時，先拉取最新的 docker image
        force_pull=True,
        # 在退出容器時自動刪除容器。
        auto_remove=True,
    )
