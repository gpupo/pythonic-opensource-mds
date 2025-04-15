"""Flow e deploy.

Requer criacao de work pool

    uv run prefect work-pool create --type Process scanear-work-pool

    uv run prefect worker start --pool "scanear-work-pool"

Execute esse arquivo e dispare o evento em outro terminal

"""

from icecream import ic
from prefect import flow
from prefect.events import DeploymentEventTrigger
from utils.prefect import PrefectEvent

ic.configureOutput(prefix="-> ", outputFunction=print)


@flow(name="scanear-flow")
def scanear_flow(message, event_data):
    ic(message)
    ic(event_data)
    event = PrefectEvent(**event_data)
    ic(event.payload)


if __name__ == "__main__":
    scanear_flow.serve(
        name="scanear-deployment",
        parameters={"message": {"automation": "trigger"}},
        triggers=[
            DeploymentEventTrigger(
                enabled=True,
                match={"prefect.resource.id": "my.external.resource"},
                expect=["scaneou"],
                parameters={
                    "event_data": "{{ event }}",
                },
            )
        ],
    )
