from app import app

from admin.form_helpers import utils
from admin.info_resources import info
from admin.resources import mod_admin
from admin.return_docs import docs

app.register_blueprint(mod_admin, url_prefix="/admin")
app.register_blueprint(info, url_prefix="/admin/info")
app.register_blueprint(utils, url_prefix="/admin/utils")
app.register_blueprint(docs, url_prefix="/admin/docs")
