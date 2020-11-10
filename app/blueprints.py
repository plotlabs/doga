from app import app

from admin.resources import mod_admin
app.register_blueprint(mod_admin, url_prefix="/admin")
