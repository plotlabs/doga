from app import app

from admin.form_helpers import utils
from admin.info_resources import info
from admin.resources import mod_admin

app.register_blueprint(mod_admin, url_prefix="/admin")
app.register_blueprint(info, url_prefix="/admin/info")
app.register_blueprint(utils, url_prefix="/admin/utils")
