import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Booking


bp = Blueprint('booking', __name__, url_prefix='/booking')


class BookingForm(fw.FlaskForm):
    name = wt.StringField('Name')
    phone = wt.StringField('WhatsApp')
    kapan = wt.DateTimeField(format="%Y-%m-%d %H:%M")
    kendaraan = wt.SelectField('Merk & Model Kendaraan dipesan', choices='All New Avanza;Inova Reborn;Inova Venturer;HiAce Commuter;HiAce Premio;Pajero Sport;Alphard'.split(';'))
    harga = wt.IntegerField('Harga')
    jemput = wt.StringField('Titik jemput')
    status = wt.StringField('Status', default='aktif') # 'batal
    acara = wt.StringField('Tujuan')

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = BookingForm(kapan=datetime.datetime.now())
    if form.validate_on_submit():
        new_book = Booking(**form.data)
        new_book.c_by = current_user.username
        new_book.save()
        return redirect('/booking')
    return render_template('booking/add.html', form=form)

@bp.route('/<id>')
def show(id):
    bookingan = get_object_or_404(Booking, Booking.id==id)
    return render_template('booking/show.html', bookingan=bookingan)

@bp.route('')
def index():
    bookings = Booking.select().order_by(Booking.id.desc())
    return render_template('booking/index.html', bookings=bookings)

