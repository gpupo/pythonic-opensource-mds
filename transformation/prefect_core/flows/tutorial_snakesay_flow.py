import os

from infra_env import env
from prefect import flow, task
from supabase import Client, create_client
from tutorial_snakesay import snake

# Load environment variables if not running in a container
if not env.is_running_in_container():
    if not env.load_env():
        raise RuntimeError("Could not load .env file for configuration")


@task
def get_orgs():
    """Task: Busca organizações do Supabase"""
    key = os.environ.get("SERVICE_ROLE_KEY")
    url = "http://localhost:8000"
    supabase = create_client(url, key)
    response = supabase.table("org").select("name").execute()
    return [f"Hello {org['name']}" for org in response.data]


@flow(log_prints=True)
def say_flow():
    """Flow: Busca orgs e diz olá para cada uma"""
    phrases = get_orgs()
    for phrase in phrases:
        result = say_task(phrase)
        print(result)


@task
def say_task(phrase: str):
    """Task 1: Usa biblioteca de packages"""
    return snake.say(phrase)


# Run the flow
if __name__ == "__main__":
    say_flow()
