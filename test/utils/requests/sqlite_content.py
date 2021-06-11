content_def = {
    "table_name": "test_all",
    "app_name": "default",
    "jwt_required": False,
}

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

columns_with_defaults = {
    "BigInteger":  {
                    "name": "test_biginteger",
                    "type": "BigInteger",
                    "nullable": "True",
                    "unique": "False",
                    "default": 123123,
                    "foreign_key": ""
                },
    "Binary": {
                    "name": "test_binary",
                    "type": "Binary",
                    "nullable": "True",
                    "unique": "False",
                    "default": 0,
                    "foreign_key": ""
             },
    "Boolean": {
                    "name": "test_boolean",
                    "type": "Boolean",
                    "nullable": "True",
                    "unique": "False",
                    "default": 0,
                    "foreign_key": ""
             },
    "DECIMAL": {
                    "name": "test_decimal",
                    "type": "DECIMAL",
                    "nullable": "True",
                    "unique": "False",
                    "default": 1.2344,
                    "foreign_key": ""
             },
    "Date": {
                    "name": "test_date",
                    "type": "Date",
                    "nullable": "True",
                    "unique": "False",
                    "default": "2021-01-01",
                    "foreign_key": ""
            },
    "DateTime": {
                    "name": "test_datetime",
                    "type": "DateTime",
                    "nullable": "True",
                    "unique": "False",
                    "default": "2021-01-01 01:01:01",
                    "foreign_key": ""
            },
    "Time": {
                    "name": "test_time",
                    "type": "Time",
                    "nullable": "True",
                    "unique": "False",
                    "default": "01:01:01",
                    "foreign_key": ""
            },
    "Enum": {
                    "name": "test_enum",
                    "type": "Enum",
                    "nullable": "True",
                    "unique": "False",
                    "default": "e1",
                    "enum": ["e1", "e2", "e3", "e4", 5],
                    "foreign_key": ""
            },
    "Float": {
                    "name": "test_float",
                    "type": "Float",
                    "nullable": "True",
                    "unique": "False",
                    "default": 1.2345,
                    "foreign_key": ""
            },
    "Integer": {
                    "name": "test_integer",
                    "type": "Integer",
                    "nullable": "True",
                    "unique": "False",
                    "default": 1,
                    "foreign_key": ""
        },
    "JSON": {
                    "name": "test_json",
                    "type": "JSON",
                    "nullable": "True",
                    "unique": "False",
                    "default": {
                        "1": "this is one",
                        "2": "this is two"
                    },
                    "foreign_key": ""
    },
    "LargeBinary": {
                    "name": "test_largebinary",
                    "type": "LargeBinary",
                    "nullable": "True",
                    "unique": "False",
                    "default": 1,
                    "foreign_key": ""
    },
    "Numeric": {
                    "name": "test_numeric",
                    "type": "Numeric",
                    "nullable": "True",
                    "unique": "False",
                    "default": 1,
                    "foreign_key": ""
    },
    "String": {
                    "name": "test_string",
                    "type": "String(300)",
                    "nullable": "True",
                    "unique": "False",
                    "default": "this"*3,
                    "foreign_key": ""
    },
    "Text": {
                    "name": "test_text",
                    "type": "Text",
                    "nullable": "True",
                    "unique": "False",
                    "default": "this"*5,
                    "foreign_key": ""
    },
    "VARCHAR": {
                    "name": "test_varchar",
                    "type": "VARCHAR",
                    "nullable": "True",
                    "unique": "False",
                    "default": "this"*3,
                    "foreign_key": ""
    },
    "ImageType": {
        "name": "test_image",
        "type": "ImageType",
        "nullable": "True",
        "unique": "False",
        "default": "",
        "foreign_key": ""
    },
}

columns_without_defaults = {

}


columns_incorrect_defaults = {

}
