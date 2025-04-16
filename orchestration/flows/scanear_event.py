from prefect.events import emit_event


def publicar_evento():
    emit_event(
        event="scaneou",  # Nome do evento
        resource={"prefect.resource.id": "my.external.resource"},
        payload={"message": {"id": 1, "name": "Carlos"}},
    )


if __name__ == "__main__":
    publicar_evento()
