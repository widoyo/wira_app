import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Booking, Customer


bp = Blueprint('booking', __name__, url_prefix='/booking')


class BookingForm(fw.FlaskForm):
    pemesan = wt.SelectField('Pemesan', validators=[DataRequired()])
    kapan = wt.DateTimeField(format="%Y-%m-%d %H:%M", 
                             validators=[DataRequired()])
    kota = wt.StringField('Kota Tujuan', validators=[DataRequired()])
    num_hari = wt.IntegerField('Berapa hari', default=1, validators=[DataRequired()])
    kendaraan = wt.SelectField('Merk & Model Kendaraan dipesan', 
                               validators=[DataRequired()],
                               choices='All New Avanza;Inova Reborn;Inova Venturer;HiAce Commuter;HiAce Premio;Pajero Sport;Alphard'.split(';'))
    harga = wt.IntegerField('Harga', validators=[DataRequired()])
    jemput = wt.StringField('Titik jemput')
    status = wt.StringField('Status', default='aktif') # 'batal

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = BookingForm(kapan=datetime.datetime.now() + datetime.timedelta(days=2))
    form.pemesan.choices = [(c.id, c.name) for c in Customer.select()]
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

