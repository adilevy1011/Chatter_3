import eventlet
from backend import create_app
if __name__=='__main__':
    app = create_app()
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0',5678)),app)
