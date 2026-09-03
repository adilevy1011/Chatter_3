from backend import create_app
from backend.config import sio


if __name__=='__main__':
    app = create_app()
    sio.run(app, host="0.0.0.0", port=5678)
