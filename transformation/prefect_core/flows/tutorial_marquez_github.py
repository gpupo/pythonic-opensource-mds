"""Flow Prefect que busca os repos da Apache no GitHub e categoriza o repo em warehouse ou other"""

# Configuração do Marquez como transporte OpenLineage
# NOTE: https://openlineage.io/docs/client/python/
import logging
import sys
import uuid
from datetime import datetime

import pytz
from openlineage.client import OpenLineageClient
from openlineage.client.run import Job, Run, RunEvent, RunState
from openlineage.client.transport.http import (
    ApiKeyTokenProvider,
    HttpConfig,
    HttpTransport,
)
from prefect import flow, task

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Configuração sem o parâmetro de compressão
    http_config = HttpConfig(
        url="http://localhost:5000",
        endpoint="/api/v1/lineage",
        verify=False,
        timeout=30,
    )

    # Como mencionado, por padrão o API não requer autenticação
    transport = HttpTransport(http_config)

    # Inicializa o cliente OpenLineage
    client = OpenLineageClient(transport=transport)

except Exception as e:
    logger.error(f"Erro ao configurar OpenLineage client: {str(e)}")
    client = None


@task(name="fetch_apache_repos")
def fetch_apache_repos():
    import requests

    try:
        # Busca os repositórios da organização Apache no GitHub
        response = requests.get("https://api.github.com/orgs/apache/repos?per_page=100")
        response.raise_for_status()  # Lança exceção para status HTTP de erro
        repos = response.json()
        return repos
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar repositórios: {str(e)}")
        return []


@task(name="categorize_repos")
def categorize_repos(repos):
    if not repos:
        logger.warning("Nenhum repositório para categorizar")
        return []

    # Lista de palavras-chave relacionadas a data warehouse
    warehouse_keywords = [
        "warehouse",
        "data",
        "analytics",
        "sql",
        "database",
        "storage",
        "hive",
        "spark",
        "hadoop",
        "kafka",
        "airflow",
        "pipeline",
        "etl",
        "query",
        "olap",
        "mart",
        "lake",
    ]

    categorized_repos = []

    try:
        for repo in repos:
            # Obtém nome e descrição
            name = repo["name"].lower()
            description = repo["description"].lower() if repo["description"] else ""

            # Verifica se alguma palavra-chave está presente
            is_warehouse = any(
                keyword in name or keyword in description
                for keyword in warehouse_keywords
            )

            category = "warehouse" if is_warehouse else "other"

            categorized_repos.append(
                {
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "category": category,
                }
            )

        return categorized_repos
    except Exception as e:
        logger.error(f"Erro ao categorizar repositórios: {str(e)}")
        return []


@flow(name="apache_repo_categorizer")
def categorize_apache_repos():
    try:
        # Gera um ID de execução único
        run_id = str(uuid.uuid4())

        # Executa o pipeline primeiro
        repos = fetch_apache_repos()
        categorized = categorize_repos(repos)

        # Registra o evento no OpenLineage se disponível
        if client is not None:
            try:
                # Formato timestamp ISO 8601 para o evento
                current_time = datetime.now(pytz.utc).isoformat()

                # Cria um evento start com listas vazias explicitamente iniciadas
                start_event = RunEvent(
                    eventType="START",
                    eventTime=current_time,
                    run=Run(runId=run_id, facets={}),
                    job=Job(
                        namespace="github", name="apache_repo_categorizer", facets={}
                    ),
                    producer="prefect",
                    inputs=[],  # Lista vazia explícita em vez de None
                    outputs=[],  # Lista vazia explícita em vez de None
                )

                # Envia o evento start
                client.emit(start_event)

                # Cria um evento complete
                complete_event = RunEvent(
                    eventType="COMPLETE",
                    eventTime=current_time,
                    run=Run(runId=run_id, facets={}),
                    job=Job(
                        namespace="github", name="apache_repo_categorizer", facets={}
                    ),
                    producer="prefect",
                    inputs=[],  # Lista vazia explícita em vez de None
                    outputs=[],  # Lista vazia explícita em vez de None
                )

                # Envia o evento complete
                client.emit(complete_event)

                logger.info(
                    f"Eventos OpenLineage emitidos com sucesso para o run ID: {run_id}"
                )

            except Exception as ol_error:
                logger.error(f"Erro ao emitir eventos OpenLineage: {str(ol_error)}")
                # Imprime o traceback para facilitar a depuração
                import traceback

                logger.error(traceback.format_exc())

        # Contagem de resultados
        warehouse_count = sum(
            1 for repo in categorized if repo["category"] == "warehouse"
        )
        other_count = len(categorized) - warehouse_count

        logger.info(f"Total repositórios: {len(categorized)}")
        logger.info(f"Repositórios de warehouse: {warehouse_count}")
        logger.info(f"Outros repositórios: {other_count}")

        return categorized
    except Exception as e:
        logger.error(f"Erro na execução do flow: {str(e)}")
        return []


if __name__ == "__main__":
    try:
        categorize_apache_repos()
    except Exception as e:
        logger.critical(f"Falha crítica na execução: {str(e)}")
        sys.exit(1)
