from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import MetaData

from admin.utils import extract_database_name

from dbs import DB_DICT


for connection_name in DB_DICT:
    connection_string = DB_DICT[connection_name]
    db_type = connection_string.split(':')[0]
    db = extract_database_name(connection_name)
    choice = input("Do you want to delete " + db_type + " database " + db + " Y/N")  # noqa 401
    if choice.lower() == 'y':
        try:
            engine = create_engine(connection_string)
            conn = engine.connect()
            MetaData().drop_all(engine)
            conn.invalidate()
            engine.dispose()
        except OperationalError as err:
            print("Could not delete " + db_type + " database " + db)
            import traceback
            traceback.print_exc()
            continue

"""
#TODO: could not find a way to import the metadata even from inside the app folder
       * maybe have a cleanup endpoint from inside the app
for table in reversed(meta.sorted_tables):

    print(table.info['bind_key'])
    #choice = input("Do you want to delete " + db_type + " table " + db + " Y/N")  # noqa 401
    #if choice.lower() == 'y':
    #    engine.execute(table.delete())
"""
