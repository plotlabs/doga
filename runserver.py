from app import app
from config import HOST, PORT

if __name__ == "__main__":
    app.run(host=HOST, use_reloader=True, port=PORT)
