# Migrations

`--autogenerate` Detecta mudanças nos modelos e gera o upgrade/downgrade automaticamente.

    uv run alembic revision --autogenerate -m "Criação do schema inicial com tabelas principais do domínio"
