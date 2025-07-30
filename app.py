from flask import Flask

from route.hello import hello_bp

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.register_blueprint(hello_bp)
