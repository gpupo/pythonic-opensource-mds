import asyncio

from prefect import flow, task
from prefect_docker.containers import (
    create_docker_container,
    get_docker_container_logs,
    remove_docker_container,
    start_docker_container,
    stop_docker_container,
)
from prefect_docker.images import pull_docker_image


@task
async def ensure_image_exists(image_name, tag):
    try:
        print(f"Pulling image: {image_name}")
        await pull_docker_image(image_name, tag)
        print(f"Successfully pulled image: {image_name}")
    except Exception as e:
        print(f"Error pulling image: {e}")
        raise


@task
async def run_container(image_name="alpine", tag="latest"):
    # Download da imagem caso inexistente
    await ensure_image_exists(image_name, tag)

    # NOTE: Objeto Container: https://docker-py.readthedocs.io/en/stable/containers.html
    container = await create_docker_container(
        image=image_name,
        entrypoint=["/bin/sh", "-c", 'echo "Hello, $MY_VAR!"'],
        # command=["echo", "Hello, container!"],
        environment=["MY_VAR=Snake"],
        # auto_remove=True,
    )
    await start_docker_container(container_id=container.id)
    logs = await get_docker_container_logs(container_id=container.id)
    print(logs)
    stop_docker_container(container_id=container.id)
    remove_docker_container(container_id=container.id)


@flow
def docker_flow():
    asyncio.run(run_container())


if __name__ == "__main__":
    docker_flow()
