invalid_jwt_table = {
    "table_name": "student",
    "connection_name": "default",
    "base_jwt": True,
    "filter_keys": ["name"],
    "columns": [
                {
                    "name": "name",
                    "type": "TEXT",
                    "nullable": "False",
                    "unique": "True",
                    "default": "",
                    "foreign_key": ""
                },
                {
                    "name": "desc",
                    "type": "TEXT",
                    "nullable": "False",
                    "unique": "True",
                    "default": "",
                    "foreign_key": ""
                }
            ]
    }