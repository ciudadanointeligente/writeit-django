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
                "slug": "instance-1"
            },
            {
                "id": 2,
                "name": "instance 2",
                "resource_uri": "/api/v1/instance/2/",
                "slug": "instance-2"
            }
        ]
    }