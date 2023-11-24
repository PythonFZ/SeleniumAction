from flask import Flask, render_template
from flask_socketio import SocketIO
import dataclasses
import threading
import uuid


def create_app() -> (Flask, SocketIO):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = uuid.uuid4().hex

    socketio = SocketIO(app)
    
    @app.route("/")
    def index():
        return render_template("index.jinja2")
        
    @socketio.on("connect")
    def on_connect():
        print("connected")
    
    @socketio.on("test")
    def on_test():
        return "test"
    
    return app, socketio
