from admin.validators import column_types


def all_coltypes():
    available_types = column_types()
    for i in [
            "INT",
            "INTEGER",
            "ARRAY",
            "BOOLEAN",
            "TEXT",
            "CLOB",
            "TIMESTAMP",
            "Interval",
            "CHAR",
            "NCHAR",
            "NVARCHAR",
            "Concatenable",
            "BINARY",
            "FLOAT",
            "BLOB",
            "REAL",
            "NUMERIC",
            "DATETIME",
            "TIME",
            "DATE",
            "BIGINT",
            "SMALLINT",
            "SmallInteger",
            "Indexable",
    ]:
        available_types.remove(i)

    available_types.append("ImageType")
    return available_types