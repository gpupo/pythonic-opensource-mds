"""Flows, tasks, events e deploys; low-code.

WARN: Este programa tem o objetivo educacional e nao esta pronto para ambiente produtivo;
Com proposito instrutivo a escrita desrespeita algumas boas praticas


Utiliza Prefect juntamente com pydantic, uv, arquitetura orientada a eventos assincronos,

INFO: Requer criacao de work pool Prefect

    uv run prefect work-pool create --type process local-process-work-pool

    uv run prefect worker start --pool "local-process-work-pool"

Execute esse arquivo e dispare o evento em outro terminal, simulando o inicio do fluxo

    uv run flow.py --serve

    uv run flow.py --trigger

NOTE: Nomes de eventos

<verboEvento>-<entidade>-<papel>

Ou, quando o componente apenas reage ao evento com uma responsabilidade clara:

<event_name>-<processor|analyzer|enricher|scanner|notifier|logger>

repository-created-notifier   → escuta "repository.created" e envia notificação
repository-prepared-enricher  → escuta "repository.prepared" e enriquece dados

- Use kebab-case ou snake_case, conforme o padrão do seu time
- Evite nomes genéricos como listener, worker, handler.
- Inclua o nome do evento ou ação como parte do nome do componente.
- Se o evento for nomeado com namespace (user.registered, order.paid), mantenha isso consistente.

NOTE: Diagrama do Fluxo

```mermaid
flowchart TD

%% Eventos
event1([repository.prepared]):::event
event2([repository.tagged]):::event


%% Deployment A
subgraph repository-prepared-deployment
    repository-prepared-flow --> repository-enrich-task:::task--> event2
end

%% Deployment B
subgraph repository-scanner-deployment
    repository-scanner-flow --> bandit-scan-task:::task
    repository-scanner-flow --> pylint-scan-task:::task
end

%% Deployment C
subgraph repository-tagged-analyzer
    repository-tagged-analysis-flow --> analyze-git-statistics-task:::task
end

%% Coreografia por eventos
event1 --> repository-prepared-flow
event2 --> repository-scanner-flow
event2 --> repository-tagged-analysis-flow

classDef event stroke:#00f
classDef task stroke:#0f0
```
"""

import ast
import os
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import yaml
from icecream import ic
from prefect import flow, serve, task
from prefect.events import DeploymentEventTrigger, emit_event
from prefect.logging import get_run_logger
from prefect.testing.utilities import prefect_test_harness
from pydantic import BaseModel, Field, computed_field
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Session, SQLModel, create_engine

# Constantes
RESOURCE_ID = "repository.resource"
UVX_PATH = os.path.expanduser("~/.cargo/bin/uvx")
PARSE_EVENT_DATA_TEMPLATE = {
    "id": "{{ event.id }}",
    "occurred": "{{ event.occurred }}",
    "event": "{{ event.event }}",
    "payload": "{{ event.payload }}",
}


# Modelos low-code com Pydantic BaseModel mas antes usando um abstrato para maior controle
class SuperDataModel(BaseModel):
    class Config:
        extra = "allow"  # Allows any additional fields
        json_encoders = {datetime: lambda v: v.isoformat()}


class PrefectEvent(SuperDataModel):
    """Evento no padrao emitido pelo Prefect."""

    occurred: datetime
    event: str
    payload: Dict[str, Any]
    id: Optional[UUID] = None
    deployment: Optional[Any] = None


class OrgData(SuperDataModel):
    id: int
    login: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None


class ProductData(SuperDataModel):
    id: int
    org_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    org: Optional[OrgData] = None


class Author(SuperDataModel):
    name: Optional[str] = None
    login: Optional[str] = None


class Commit(SuperDataModel):
    message: str
    committedDate: datetime
    author: Author


class BranchTarget(SuperDataModel):
    history: Optional[List[Commit]] = None


class Branch(SuperDataModel):
    name: str
    target: Optional[BranchTarget] = None


class PullRequest(SuperDataModel):
    title: str
    mergedAt: datetime
    mergedBy: Author


class RepositoryData(SuperDataModel):
    """repository git-based data.

    id: String
    name: String
    product:
        name: String
        org:
            name: String
    pullRequests:
      - title: String
        mergedAt: DateTime
        mergedBy:
          login: String
    defaultBranchRef:
      name: String
      target:
        history:
          - message: String
            committedDate: DateTime
            author:
              name: String

    """

    id: str
    name: str
    product: Optional[ProductData] = None
    pullRequests: List[PullRequest]
    defaultBranchRef: Branch


class RepositoryContainer(SuperDataModel):
    """Persiste as informacoes em banco de dados"""

    id: int
    repository_data: RepositoryData = None


def emit_repository_event(event_name: str, repository_container: RepositoryContainer):
    """Dispara um evento contextualizado com payload estruturado"""
    return emit_event(
        event=event_name,
        resource={"prefect.resource.id": RESOURCE_ID},
        payload=repository_container.model_dump(include={"id"}),
    )


### TASKS ###


@task
def uvx_run(
    command, target_path, output_format="json2", output_file=None, capture_output=True
):
    """Execute a UVX command on the specified target path."""
    logger = get_run_logger()
    logger.info(f"Starting {command} via UVX on: {target_path}")

    cmd = [UVX_PATH, command]

    if output_format:
        cmd.append(f"--output-format={output_format}")

    if output_file:
        cmd.append(f"--output={output_file}")

    cmd.append(target_path)

    result = subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
        check=False,
    )
    logger.debug(result)
    return result


def get_repository_container_by_id(id: int) -> RepositoryContainer:
    # TODO: implementar usando persistencia
    repository_data = fixture_with_repository_sample(id)
    repository_container = RepositoryContainer(id=id, repository_data=repository_data)
    return repository_container


def fixture_with_repository_sample(id: int) -> RepositoryData:
    """Simulando acesso ao dtw."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(script_dir, "repository_sample.yaml")

    with open(yaml_path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
    repo = RepositoryData(**data["data"]["repository"])
    return repo


def event_unpack(**kwargs) -> Tuple[PrefectEvent, RepositoryContainer]:
    """Transforma em objetos as info recebidas em evento."""
    occurred = kwargs.get("occurred")
    event = kwargs.get("event")
    payload = kwargs.get("payload")
    id_val = kwargs.get("id")
    deployment_parameters = kwargs.get("deployment")

    if isinstance(payload, str):
        payload = ast.literal_eval(payload)

    prefect_event = PrefectEvent(
        deployment=deployment_parameters,
        occurred=occurred,
        event=event,
        payload=payload,
        id=id_val,
    )

    repository_container = get_repository_container_by_id(
        prefect_event.payload.get("id")
    )

    return prefect_event, repository_container


@task(name="repository-enrich-task")
def repository_enrich_task(repository_container: RepositoryContainer):
    logger = get_run_logger()
    logger.info(f"Repository enriched: {repository_container.id}")


@task(name="bandit-scan-task")
def bandit_scan_task(repository_container: RepositoryContainer):
    print(f"Access {repository_container.id}...")


@task(name="pylint-scan-task")
def pylint_scan_task(repository_container: RepositoryContainer):
    """Run Pylint static code analysis on the repository."""
    logger = get_run_logger()
    logger.info("Refactory!")
    # repo_path = getattr(repository_container, "path", "/tmp/default_repo")
    # scan_path = f"{repo_path}/web"
    # logger.info(f"Starting Pylint scan on: {scan_path}")
    # result = uvx_run("pylint", scan_path, output_file="pylint_report.json")
    # logger.debug(result)


@task(name="analyze-git-statistics-task")
def analyze_git_statistics_task(repository_container: RepositoryContainer):
    print(f"Analyzing Git stats for repository {repository_container.id}")


### FLOWS ###
@flow(name="repository-prepared-flow")
def repository_prepared_flow(
    info,
    id,
    occurred,
    event,
    payload,
):
    """Flow que processa o evento repository.prepared"""
    logger = get_run_logger()
    logger.info(
        f"Processing event {event} for repository {payload.get('repository', {}).get('id')}"
    )

    # Desempacotando o evento
    raw_event, repository_container = event_unpack(
        occurred=occurred,
        event=event,
        payload=payload,
        id=id,
    )
    repository_enrich_task(repository_container)
    # NOTE: Dispara evento de tagged
    emit_repository_event("repository.tagged", repository_container)


@flow(name="repository-scanner-flow")
def repository_scanner_flow(
    info,
    id,
    occurred,
    event,
    payload,
):
    # Desempacotando o evento
    raw_event, repository_container = event_unpack(
        occurred=occurred,
        event=event,
        payload=payload,
        id=id,
    )
    bandit_scan_task(repository_container)
    pylint_scan_task(repository_container)
    # Emite novo evento ...


@flow(name="repository-tagged-analysis-flow")
def repository_tagged_analysis_flow(
    info,
    id,
    occurred,
    event,
    payload,
):
    # Desempacotando o evento
    raw_event, repository_container = event_unpack(
        occurred=occurred,
        event=event,
        payload=payload,
        id=id,
    )
    analyze_git_statistics_task(repository_container)


###  INFO: Testes https://docs.prefect.io/v3/develop/test-workflows


def test_repository_enrich_task():
    pass


### Deployment ###
def create_event_deployment(flow, name: str, expected_event: str):
    """Factory function to create event-triggered deployments.

    NOTE: https://reference.prefect.io/prefect/flows/#prefect.flows.Flow.to_deployment

    """
    return flow.to_deployment(
        name=name,
        parameters={"info": {"automation": "trigger"}},
        triggers=[
            DeploymentEventTrigger(
                enabled=True,
                match={"prefect.resource.id": RESOURCE_ID},
                expect=[expected_event],
                parameters=PARSE_EVENT_DATA_TEMPLATE,
            )
        ],
    )


def serve_deployments():
    """Creates a deployment for the flow and starts a long-running process.

    NOTE: https://docs.prefect.io/v3/deploy/run-flows-in-local-processes#serve-a-flow
    """
    repository_prepared_deployment = create_event_deployment(
        repository_prepared_flow,
        "repository-prepared-deployment",
        "repository.prepared",
    )
    repository_scanner_deployment = create_event_deployment(
        repository_scanner_flow,
        "repository-scanner-deployment",
        "repository.tagged",
    )

    repository_tagged_analysis_deployment = create_event_deployment(
        repository_tagged_analysis_flow,
        "repository-tagged-analyzer",
        "repository.tagged",
    )

    serve(
        repository_prepared_deployment,
        repository_scanner_deployment,
        repository_tagged_analysis_deployment,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Repository data tool")
    parser.add_argument("--serve", action="store_true", help="Serve deployments")
    parser.add_argument(
        "--trigger", action="store_true", help="Trigger repository.prepared event"
    )
    args = parser.parse_args()

    if args.serve:
        serve_deployments()
    elif args.trigger:
        # Simula o disparo do evento com o repository 1
        repository_container = RepositoryContainer(id=1)
        emit_repository_event("repository.prepared", repository_container)
        print("Evento 'repository.prepared' disparado.")
    else:
        # INFO: usado para desenvolvimento e depuracao
        repository_container = get_repository_container_by_id(1)
        ic(
            emit_repository_event(
                "repository.prepared", repository_container.repository_data
            )
        )
