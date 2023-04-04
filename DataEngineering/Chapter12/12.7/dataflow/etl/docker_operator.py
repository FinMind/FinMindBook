from airflow.operators.docker_operator import (
    DockerOperator,
)


def create_docker_operator_task() -> DockerOperator:
    return DockerOperator(
        task_id="DockerOperator",
        image="continuumio/miniconda3:4.7.12",
        command="echo DockerOperator",
        # 在退出容器時自動刪除容器。
        auto_remove=True,
    )
