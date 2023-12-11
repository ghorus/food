from foodInnerFolder import app,socketio
import eventlet
import eventlet.wsgi
eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)

if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app,debug=True)
