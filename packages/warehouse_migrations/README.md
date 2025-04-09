# Migrations

Alembic provides for the creation, management, and invocation of change management
scripts for a relational database, using SQLAlchemy as the underlying engine.

`--autogenerate`

Detecta mudanças nos modelos e gera o upgrade/downgrade automaticamente.

    uv run alembic revision --autogenerate -m "Criação do schema inicial com tabelas principais do domínio"

Rodar as migrations

    uv run alembic upgrade head

[Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
