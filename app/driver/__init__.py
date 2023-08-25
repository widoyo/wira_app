import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from werkzeug.utils import secure_filename
from flask_login import current_user
from wtforms.validators import DataRequired
from app.models import Driver


bp = Blueprint('driver', __name__, url_prefix='/driver')


class DriverForm(fw.FlaskForm):
    name = wt.StringField('Name')
    phone = wt.StringField('WhatsApp')
    addr1 = wt.StringField('Alamat')
    addr1 = wt.StringField('Kota')
    ktp = wt.FileField()

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = DriverForm()
    if form.validate_on_submit():
        new_cust = Driver(**form.data)
        new_cust.c_by = current_user.username
        new_cust.save()
        return redirect('/driver')
    return render_template('driver/add.html', form=form)

@bp.route('/<id>')
def show(id):
    driver = get_object_or_404(Driver, Driver.id==id)
    return render_template('driver/show.html', driver=driver)

@bp.route('')
def index():
    drivers = Driver.select().order_by(Driver.id.desc())
    return render_template('driver/index.html', drivers=drivers)

