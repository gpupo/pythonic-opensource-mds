import logging
import os
from logging.config import fileConfig

from alembic import context
from icecream import ic
from infra_env import env
from sqlalchemy import create_engine
from warehouse_objects.org import *

# Load environment variables if not running in a container
if not env.is_running_in_container():
    if not env.load_env():
        raise RuntimeError("Could not load .env file for configuration")


def get_url():
    """Generate a URL from the environment variables, Tenant ID mode."""
    return "postgresql://%s.%s:%s@%s:%s/%s" % (
        os.environ["POSTGRES_USER"],
        os.environ["POOLER_TENANT_ID"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_STATIC_HOST"],
        os.environ["POSTGRES_PORT"],
        os.environ["POSTGRES_DB"],
    )


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.runtime.migration")
logger.setLevel(logging.INFO)


target_metadata = SQLModel.metadata


def include_object(object, name, type_, reflected, compare_to):
    """Ignora qualquer tabela do schema auth"""
    if type_ == "table" and object.schema == "auth":
        logger.info(f"Ignorando objetos do schema {object.schema}:{name}")
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # render_item=render_item,
        compare_server_default=False,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Objeto principal para criacao de migrations."""
    connectable = create_engine(get_url())
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=False,
            compare_server_default=True,
            # include_name=None,
            include_object=include_object,
            # render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
