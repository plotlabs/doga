from app import app
from admin.utils import set_jwt_secret_key
from config import HOST, PORT

if __name__ == "__main__":
    set_jwt_secret_key()
    app.run(host=HOST, port=PORT, use_reloader=True, threaded=True)
