from prefect import flow, task  # Prefect flow and task decorators
from tutorial_snakesay import snake


@flow(log_prints=True)
def say_flow(phrases: list[str]):
    """Flow: Aciona uma ou mais tasks"""
    for p in phrases:
        # Call Task 1
        said = say_task(phrase=p)

        # Print the result
        print(f"{said}")


@task
def say_task(phrase: str):
    """Task 1: Usa biblioteca de packages"""
    return snake.say(phrase)


# Run the flow
if __name__ == "__main__":
    say_flow(["Hello from Prefect Flow!"])
