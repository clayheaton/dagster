import logging
import os

from dagster._core.definitions.reconstruct import ReconstructableRepository
from dagster_test.dagster_airflow.custom_operator import CustomOperator
from dagster_test.test_project import get_test_project_environments_path

from dagster_airflow_tests.marks import requires_airflow_db
from dagster_airflow_tests.test_factory.utils import validate_pipeline_execution
from dagster_airflow_tests.test_fixtures import (
    dagster_airflow_custom_operator_pipeline,  # noqa: F401 (fixture)
)


@requires_airflow_db
def test_my_custom_operator(
    dagster_airflow_custom_operator_pipeline,  # noqa: F811 (fixture)
    caplog,
):
    caplog.set_level(logging.INFO, logger="CustomOperatorLogger")
    pipeline_name = "demo_pipeline_s3"
    operator = CustomOperator

    environments_path = get_test_project_environments_path()

    results = dagster_airflow_custom_operator_pipeline(
        pipeline_name=pipeline_name,
        recon_repo=ReconstructableRepository.for_module(
            "dagster_test.test_project.test_pipelines.repo", pipeline_name
        ),
        operator=operator,
        environment_yaml=[
            os.path.join(environments_path, "env.yaml"),
            os.path.join(environments_path, "env_s3.yaml"),
        ],
    )
    validate_pipeline_execution(results)

    log_lines = 0
    for record in caplog.records:
        if record.name == "CustomOperatorLogger":
            log_lines += 1
            assert record.message == "CustomOperator is called"

    assert log_lines == 2
