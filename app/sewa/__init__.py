import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Sewa


bp = Blueprint('sewa', __name__, url_prefix='/sewa')


class BookingForm(fw.FlaskForm):
    name = wt.StringField('Name')
    phone = wt.StringField('WhatsApp')
    kapan = wt.DateTimeField(format="%Y-%m-%d %H:%M")
    kendaraan = wt.SelectField('Merk & Model Kendaraan dipesan', choices='All New Avanza;Inova Reborn;Inova Venturer;HiAce Commuter;HiAce Premio;Pajero Sport;Alphard'.split(';'))
    harga = wt.IntegerField('Harga')
    jemput = wt.StringField('Titik jemput')
    status = wt.StringField('Status', default='aktif') # 'batal

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = BookingForm(kapan=datetime.datetime.now())
    if form.validate_on_submit():
        new_sewa = Sewa(**form.data)
        new_sewa.c_by = current_user.username
        new_sewa.save()
        return redirect('/sewa')
    return render_template('sewa/add.html', form=form)

@bp.route('/<id>')
def show(id):
    sewa = get_object_or_404(Sewa, Sewa.id==id)
    return render_template('sewa/show.html', sewa=sewa)

@bp.route('')
def index():
    sewas = Sewa.select().order_by(Sewa.id.desc())
    return render_template('sewa/index.html', sewas=sewas)

