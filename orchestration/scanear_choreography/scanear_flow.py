"""Flow e deploy.

Requer criacao de work pool

    uv run prefect work-pool create --type Process scanear-work-pool

    uv run prefect worker start --pool "scanear-work-pool"

Execute esse arquivo e dispare o evento em outro terminal

"""

# ic.configureOutput(prefix="-> ", outputFunction=print)
import ast

from icecream import ic
from prefect import flow
from prefect.events import DeploymentEventTrigger
from utils.prefect import parse_event_data


@flow(name="scanear-flow")
def scanear_flow(
    deployment_parameters,
    id,
    occurred,
    event,
    payload,
):
    event = parse_event_data(
        deployment=deployment_parameters,
        occurred=occurred,
        event=event,
        payload=payload,
        id=id,
    )
    ic(event)
    ic(event.message)


EVENT_PARSE_PARAMETERS_TEMPLATE = {
    "id": "{{ event.id }}",
    "occurred": "{{ event.occurred }}",
    "event": "{{ event.event }}",
    "payload": "{{ event.payload }}",
}
if __name__ == "__main__":
    scanear_flow.serve(
        name="scanear-deployment",
        parameters={"deployment_parameters": {"automation": "trigger"}},
        triggers=[
            DeploymentEventTrigger(
                enabled=True,
                match={"prefect.resource.id": "my.external.resource"},
                expect=["scaneou"],
                parameters=EVENT_PARSE_PARAMETERS_TEMPLATE,
            )
        ],
    )
