import hashlib
import time
import datetime
import peewee as pw
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Sewa, Driver, Mobil, Booking, BayaranSewa, JASA_CHOICES
from app.kas import KasInForm

bp = Blueprint('sewa', __name__, url_prefix='/sewa')


class SewaForm(fw.FlaskForm):
    lokasi_jemput = wt.StringField('Lokasi Jemput', validators=[wt.validators.DataRequired()])
    waktu_jemput = wt.DateTimeField(format="%Y-%m-%d %H:%M", validators=[wt.validators.DataRequired()])
    est_tiba = wt.DateTimeField(format="%Y-%m-%d %H:%M")
    mobil = wt.SelectField('Mobil', validators=[wt.validators.DataRequired()])
    jasa = wt.SelectField('Jasa', choices=JASA_CHOICES)
    num_hari = wt.IntegerField('Durasi')
    driver = wt.SelectField('Driver')
    harga = wt.IntegerField('Harga', validators=[wt.validators.DataRequired()])
    kota = wt.StringField('Kota')
    keterangan = wt.StringField('Name')
    km_berangkat = wt.IntegerField()
    km_tiba = wt.IntegerField()
    
class BeaForm(fw.FlaskForm):
    bea_supir = wt.IntegerField()
    bea_tol = wt.IntegerField()
    bea_bensin = wt.IntegerField()
    bea_lain = wt.IntegerField()
    
    
class PaymentForm(fw.FlaskForm):
    tanggal = wt.DateField()
    nilai = wt.IntegerField()
    
@bp.route('/add/<booking_id>', methods=['POST', 'GET'])
def add(booking_id):
    print(booking_id)
    booking = Booking.get(int(booking_id))
    form = SewaForm(waktu_jemput=booking.waktu_jemput, harga=booking.harga, 
                    kota=booking.kota, num_hari=booking.num_hari,
                    lokasi_jemput=booking.lokasi_jemput)
    form.mobil.choices = [(c.id, "{} {}".format(c.nopol, c.model)) for c in Mobil.select().order_by(Mobil.nopol.asc())]
    form.driver.choices = [(d.id, d.name) for d in Driver.select()]
    form.jasa.data = booking.jasa
    #form.jemput.value = booking.kapan
    if form.validate_on_submit():
        new_sewa = Sewa(**form.data)
        new_sewa.booking = booking
        new_sewa.c_by = current_user.username
        new_sewa.save()
        return redirect('/sewa')
    return render_template('sewa/add.html', form=form, booking=booking)

@bp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    try:
        sewa = Sewa.get(int(id))
    except pw.DoesNotExist:
        return add(id)
    payment_form = PaymentForm()
    if payment_form.validate_on_submit():
        bs = BayaranSewa(**payment_form.data)
        bs.sewa = sewa
        bs.c_by = current_user.username
        bs.save()
        return redirect("/sewa/{}".format(sewa.id))
    return render_template('sewa/show.html', sewa=sewa, payform=payment_form)

@bp.route('')
def index():
    bulan = request.args.get('bln') and datetime.datetime.strptime(request.args.get('bln'), '%Y-%m') or datetime.date.today()
    start = bulan.replace(day=1)
    if bulan.month == datetime.date.today().month:
        end = datetime.date.today()
    else:
        end = (bulan.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    prev = (bulan - datetime.timedelta(days=1)).strftime('%Y-%m')
    next = (bulan + datetime.timedelta(days=32)).strftime('%Y-%m')
    form = KasInForm()
    sewas = Sewa.select().where(Sewa.waktu_jemput.between(start, end)).order_by(Sewa.id.desc())
    return render_template('sewa/index.html', sewas=sewas, form=form, bulan=bulan, prev=prev, next=next)

