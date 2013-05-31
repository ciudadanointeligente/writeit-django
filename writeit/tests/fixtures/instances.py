def get_all():
    return {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 2
        },
        "objects": [
            {
                "id": 1,
                "name": "instance 1",
                "resource_uri": "/api/v1/instance/1/",
                "slug": "instance-1",
                "messages_uri": "/api/v1/instance/1/messages/"
            },
            {
                "id": 2,
                "name": "instance 2",
                "resource_uri": "/api/v1/instance/2/",
                "slug": "instance-2",
                "messages_uri": "/api/v1/instance/2/messages/"
            }
        ]
    }


def get_messages_for_instance1():
    return {
            "answers": [
                {
                    "content": "si es una prueba",
                    "created": "2013-05-15",
                    "id": 1,
                    "resource_uri": ""
                },
                {
                    "content": "asdasdasd",
                    "created": "2013-05-16",
                    "id": 2,
                    "resource_uri": ""
                }
            ],
            "author_email": "falvarez@votainteligente.cl",
            "author_name": "Felipi poo",
            "content": "probando probando",
            "id": 1,
            "public": True,
            "resource_uri": "/api/v1/message/1/",
            "slug": "esto-es-una-prueba",
            "subject": "esto es una prueba",
            "writeitinstance": "/api/v1/instance/1/"
            }
