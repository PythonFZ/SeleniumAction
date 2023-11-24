from flask import Flask, render_template
from flask_socketio import SocketIO
import dataclasses
import threading


def create_app() -> (Flask, SocketIO):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret!"

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




# @dataclasses.dataclass
# class MyServer:
#     app: Flask = None
#     socketio: SocketIO = None
#     port: int = 5000

#     _socketio_thread: threading.Thread = None

#     def __post_init__(self) -> None:
#         self.app = Flask(__name__)
#         self.app.config["SECRET_KEY"] = "secret!"
#         self.socketio = SocketIO(self.app)

#         @self.app.route("/")
#         def index():
#             return render_template("index.html")

#         self._socketio_thread = threading.Thread(
#             target=self.socketio.run,
#             args=(self.app,),
#             kwargs={"debug": True, "port": self.port, "host": "0.0.0.0"},
#         )
#         self._socketio_thread.start()

        
