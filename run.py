from foods import app,socketio
import eventlet
import eventlet.wsgi
eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

if __name__ == "__main__":
    app.run()
    socketio.run(app)
