DB_DICT = {
    "default": "sqlite:////tmp/default.db",
    "tempapp": "postgresql+psycopg2://postgres:password@localhost:5432/tempapp",
}


ALEMBIC_LIST = [
    "AlembicVersionDefault",
    "AlembicVersionTempapp",
]
