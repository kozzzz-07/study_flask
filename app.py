from flask import Flask

from route.hello import hello_bp
from infra.client.db_client import db_bp

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.register_blueprint(hello_bp)
app.register_blueprint(db_bp)
