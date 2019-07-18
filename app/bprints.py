from app import app
from admin.resources import get_admin_bp


def init_bps():
    admin_bp = get_admin_bp()
    app.register_blueprint(admin_bp.blueprint)

