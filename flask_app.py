from flask import Flask


def register_blueprints(flask_app):
    from app.api import create_blueprint
    flask_app.register_blueprint(create_blueprint(), url_prefix='/api')


def create_app():
    flask_app = Flask(__name__)

    register_blueprints(flask_app)

    return flask_app


app = create_app()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

