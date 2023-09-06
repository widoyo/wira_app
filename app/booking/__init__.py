import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Booking, Customer, JASA_CHOICES


bp = Blueprint('booking', __name__, url_prefix='/booking')


class BookingForm(fw.FlaskForm):
    pemesan = wt.SelectField('Pemesan', validators=[DataRequired()])
    waktu_jemput = wt.DateTimeField(format="%Y-%m-%d %H:%M", 
                             validators=[DataRequired()])
    kota = wt.StringField('Kota Tujuan', validators=[DataRequired()])
    jasa = wt.SelectField('Jasa', choices=JASA_CHOICES)
    num_hari = wt.IntegerField('Berapa hari', default=1, validators=[DataRequired()])
    kendaraan = wt.SelectField('Merk & Model Kendaraan dipesan', 
                               validators=[DataRequired()],
                               choices='All New Avanza;Inova Reborn;Inova Venturer;HiAce Commuter;HiAce Premio;Pajero Sport;Alphard;Lainnya'.split(';'))
    harga = wt.IntegerField('Harga', validators=[DataRequired()])
    lokasi_jemput = wt.StringField('Lokasi jemput')
    status = wt.StringField('Status', default='aktif') # 'batal

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = BookingForm(waktu_jemput=datetime.datetime.now() + datetime.timedelta(days=2))
    form.pemesan.choices = [('', 'Pilih Customer')]+[(c.id, '{} /{}'.format(c.name, c.phone)) for c in Customer.select().order_by(Customer.name.asc())]
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

