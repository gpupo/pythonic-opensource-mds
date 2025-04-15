"""Flow e deploy.

Requer criacao de work pool

    uv run prefect work-pool create --type Process scanear-work-pool

    uv run prefect worker start --pool "scanear-work-pool"

"""

from icecream import ic
from prefect import flow
from prefect.events import DeploymentEventTrigger


@flow(name="scanear-flow")
def scanear_flow(message: dict):
    print(f"Processando mensagem: {message}")


if __name__ == "__main__":
    scanear_flow.serve(
        name="scanear-deployment",
        parameters={"message": {"Name": "Marvin"}},
        triggers=[
            DeploymentEventTrigger(
                enabled=True,
                match={"prefect.resource.id": "my.external.resource"},
                expect=["scaneou"],
                parameters={
                    "param_1": "{{ event }}",
                },
            )
        ],
    )
