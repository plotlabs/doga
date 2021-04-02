invalid_constraint_unique = {
    "table_name": "student",
    "app_name": "test_db",
    "jwt_required": True,
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
