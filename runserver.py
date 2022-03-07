from app import app
from admin.utils import set_jwt_secret_key
from config import HOST, PORT

if __name__ == "__main__":
    set_jwt_secret_key()
    debug = True
    app.run(
        host=HOST,
        port=PORT,
        debug=debug,
        use_reloader=debug,
        threaded=True,
    )
