""" Simula um evento de diretorio com repo https://github.com/apache/tvm preparado """
from prefect.events import emit_event


def publicar_evento():
    emit_event(
        event="repository.prepared",
        resource={"prefect.resource.id": "my.external.resource"},
        payload={"message": {
            "repository": "tvm",
            "path": "/tmp/pythonic-opensource-mds/apache/tvm",
            "id": "apache-tvm",
            "url":"https://github.com/apache/tvm",
        }},
    )


if __name__ == "__main__":
    publicar_evento()
