from foodInnerFolder import app,socketio
import eventlet
import eventlet.wsgi
eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 8000)),
                          certfile='cert.crt',
                          keyfile='private.key',
                          server_side=True),
        app)

if __name__ == "__main__":
    app.run()
    socketio.run(app)
