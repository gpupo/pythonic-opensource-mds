"""Flow e deploy.

Requer criacao de work pool

    uv run prefect work-pool create --type Process scanear-work-pool

    uv run prefect worker start --pool "scanear-work-pool"

Execute esse arquivo e dispare o evento em outro terminal

NOTE: Nomes

<verboEvento>-<entidade>-<papel>

order-created-notifier        → escuta "order.created" e envia notificação
payment-confirmed-logger      → escuta "payment.confirmed" e registra log
user-registered-enricher      → escuta "user.registered" e enriquece dados

repository-prepared-enricher    → escuta "repository.prepared" e enriquece dados

Ou, quando o componente apenas reage ao evento com uma responsabilidade clara:

<event_name>-<processor|analyzer|enricher|scanner>

NOTE: Dicas extras:

    Use kebab-case ou snake_case, conforme o padrão do seu time ou ferramenta (ex: Docker, Kubernetes, Prefect).

    Evite nomes genéricos como listener, worker, handler.

    Inclua o nome do evento ou ação como parte do nome do componente.

    Se o evento for nomeado com namespace (user.registered, order.paid), mantenha isso consistente.

NOTE # Fluxo

```mermaid
flowchart TD

%% Eventos
event1([repository.prepared]):::event
event2([repository.tagged]):::event


%% Deployment
subgraph repository-prepared-deployment
    flowA[repository-prepared-flow]
    flowA --> repository-enrich-task:::task--> event2
end

%% Deployment
subgraph repository-scanner-deployment
    flowB[repository-scanner-flow]
    flowB --> bandit-scan-task:::task
    flowB --> pylint-scan-task:::task
end

%% Deployment
subgraph repository-tagged-analyzer
    flowC[repository-tagged-analysis-flow]
    taskC[analyze-git-statistics-task]:::task
    flowC --> taskC
end

%% Coreografia por eventos
event1 --> flowA
event2 --> flowB
event2 --> flowC

classDef event stroke:#00f
classDef task stroke:#0f0
```
"""

# ic.configureOutput(prefix="-> ", outputFunction=print)
from icecream import ic
from prefect import flow,serve
from prefect.events import DeploymentEventTrigger
from utils.prefect import PARSE_EVENT_DATA_TEMPLATE, parse_event_data
from prefect.events import emit_event

@task(name="repository-enrich-task")
def repository_enrich_task(repository_data):
    print(f"Visiting {repository_data.url}...")
    emit_event(
        event="repository.tagged",
        resource={"prefect.resource.id": "my.external.resource"},
        payload={"message": repository_data},
    )

@flow(name="repository-prepared-flow")
def repository_prepared_flow(
    info,
    id,
    occurred,
    event,
    payload,
):
    event = parse_event_data(
        occurred=occurred,
        event=event,
        payload=payload,
        id=id,
    )
    repository_enrich_task(event.message)

@task(name="bandit-scan-task")
def bandit_scan_task(repository_data):
    print(f"Access {repository_data.path}...")

@task(name="pylint-scan-task")
def pylint_scan_task(repository_data):
    print(f"Access {repository_data.path}...")


@flow(name="repository-scanner-flow")
def repository_scanner_flow(
    info,
    id,
    occurred,
    event,
    payload,
):
    event = parse_event_data(
        occurred=occurred,
        event=event,
        payload=payload,
        id=id,
    )
    bandit_scan_task(event.message)
    pylint_scan_task(event.message)

if __name__ == "__main__":

    
    repository_prepared_deploy = repository_prepared_flow.to_deployment(
        name="repository-prepared-deployment",
        parameters={"info": {"automation": "trigger"}},
        triggers=[
            DeploymentEventTrigger(
                enabled=True,
                match={"prefect.resource.id": "my.external.resource"},
                expect=["repository.prepared"],
                parameters=PARSE_EVENT_DATA_TEMPLATE,
            )
        ],
    )

    serve(repository_prepared_deploy)
