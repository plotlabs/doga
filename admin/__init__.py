from admin.utils import migrate as run_migration


@app.before_first_request
def run_db_function():
    subprocess.run(['flask', 'db', 'init', '--multidb'])
    subprocess.run(['flask', 'db', 'migrate'])
    subprocess.run(['flask', 'db', 'upgrade'])


@app.teardown_request
def teardown(request):
    run_migration()
    global to_reload
    to_reload = True
