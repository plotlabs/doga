"""Test content for `admin/content/types endpoint
"""
# Valid Content
valid_content = {
    "table_name": "test_table",
    "app_name": "default",
    "columns": [
        {
            "name": "name",
            "type": "String(32)",
            "nullable": "False",
            "unique": "True",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "desc",
            "type": "String(32)",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "credits",
            "type": "BigInteger",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "active",
            "type": "Integer",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "dob",
            "type": "DateTime",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        }
    ]
}

# Invalid Content
invalid_boolean_column = {
    "table_name": "test_table",
    "app_name": "default",
    "columns": [
        {
            "name": "name",
            "type": "String(32)",
            "nullable": "False",
            "unique": "True",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "desc",
            "type": "String(32)",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "credits",
            "type": "BigInteger",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "active",
            "type": "Boolean",
            "nullable": "False",
            "unique": "False",
            "default": "false",
            "foreign_key": ""
        },
        {
            "name": "dob",
            "type": "DateTime",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        }
    ]
}

invalid_filter_keys = {
    "table_name": "student",
    "app_name": "test_db_test",
    "base_jwt": True,
    "filter_keys": ["invalid_key"],
    "columns": [
        {
            "name": "name",
            "type": "TEXT",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "id",
            "type": "TEXT",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        }
    ]
}

invalid_column_type = {
    "table_name": "student",
    "app_name": "default",
    "filter_keys": ["desc"],
    "columns": [
        {
            "name": "name",
            "type": "TEXT",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "desc",
            "type": "INVALIDTYPE",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        }
    ]
}

incorrect_filter_keys = {
    "table_name": "student",
    "app_name": "default",
    "jwt_required": False,
    "filter_keys": ["desc"],
    "columns": [
        {
            "name": "name",
            "type": "TEXT",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        },
        {
            "name": "id",
            "type": "Integer",
            "nullable": "False",
            "unique": "False",
            "default": "",
            "foreign_key": ""
        }
    ]
}
