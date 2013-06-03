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
                "meta": {
                "limit": 20,
                "next": None,
                "offset": 0,
                "previous": None,
                "total_count": 2
            },
            "objects": [
                    {
                        "answers": [ ],
                        "author_email": "luisfelipealvarez@gmail.com",
                        "author_name": "Felipi poo",
                        "content": "Quiero probar esto",
                        "id": 1,
                        "public": True,
                        "resource_uri": "/api/v1/message/1/",
                        "slug": "probando-probando-2",
                        "subject": "Probando probando",
                        "writeitinstance": "/api/v1/instance/1/"
                    },
                    {
                        "answers": [ ],
                        "author_email": "ncristi@votainteligente.cl",
                        "author_name": "Nicolas Cristi",
                        "content": "Buena!! Felicitaciones!",
                        "id": 2,
                        "public": True,
                        "resource_uri": "/api/v1/message/2/",
                        "slug": "y-q-tanto-2",
                        "subject": "Y? Q tanto?",
                        "writeitinstance": "/api/v1/instance/1/"
                    }
                ]
            }
