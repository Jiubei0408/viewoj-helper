from flask import Blueprint

from app.api import pta


def create_blueprint():
    bp = Blueprint('api', __name__)

    pta.api.register(bp)
    return bp
