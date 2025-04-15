from prefect.automations import Automation
from prefect.events.actions import CancelFlowRun
from prefect.events.schemas.automations import EventTrigger

# creating an automation
automation = Automation(
    name="scanear-automation",
    trigger=EventTrigger(
        expect={"scaneou"},
        match={
            "prefect.resource.id": "prefect.flow-run.*",
        },
        posture="Reactive",
        threshold=5,
    ),
    actions=[CancelFlowRun()],
).create()
print(automation)
