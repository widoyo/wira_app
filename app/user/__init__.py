from flask import Blueprint, render_template

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('')
def index():
    return render_template('/user/index.html')