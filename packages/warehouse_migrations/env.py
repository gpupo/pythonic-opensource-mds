import os
from logging.config import fileConfig

from alembic import context
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


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    """Ignora qualquer tabela do schema auth"""
    if type_ == "table" and object.schema == "auth":
        return False
    return True


def render_item_with_comments(type_, obj, autogen_context):
    """Para que o alembic revision autogenerate gere as descrições."""
    if type_ == "column" and obj.comment:
        autogen_context.imports.add("from sqlalchemy import Column")
        return f"sa.Column({repr(obj.type)}, comment={repr(obj.comment)})"
    return False


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=include_object,
            **{
                "render_item": render_item_with_comments
            },  # esta linha ativa os comentários
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
