from app import app

from app.utils import migrate as run_migration

import subprocess


@app.before_first_request
def run_db_function():
    subprocess.run(["flask", "db", "init", "--multidb"])
    subprocess.run(["flask", "db", "migrate"])
    subprocess.run(["flask", "db", "upgrade"])


@app.teardown_request
def teardown(request):
    run_migration()
