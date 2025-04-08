# Pythonic, 100% Open Source, Modern Data Stack, 2025

![Map Description](doc/map.png)

## Data Ingestion

TODO: Meltano setup

## Data Warehouse

### Migrations

`./packages/warehouse_migrations` usa [Alembic](https://alembic.sqlalchemy.org/) para
gerenciar migrations do modelo definido em `./packages/warehouse_objects`

INFO: Doc de uso no README do componente.

## Packages

#### Python Libs

Cada Lib e um `uv workspace`

- warehouse_objects: ORM da plataforma

## Data Transformation

Trigger flows em schedules, eventos externos

> [!IMPORTANT] Requer o uso de [uv](https://docs.astral.sh/uv/) para Python environment.

TODO: Prefect setup

## Cluster config (Docker Compose)

- PostgreSQL: postgresql://postgres:postgres@localhost:5432/appdb
- Valley: redis://localhost:6379
- Supabase: http://localhost:3000
- Superset: http://localhost:8088

## Install

TODO: escrever o roteiro de novas instalacoes

    git clone ...

    cd ...

    git submodule update --init --recursive

Copy the fake env vars

    cp .env.example .env

Pull the latest images

    docker compose pull

Start the services (in detached mode)

    docker compose up -d
