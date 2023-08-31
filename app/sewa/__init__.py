import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Sewa, Customer, Mobil


bp = Blueprint('sewa', __name__, url_prefix='/sewa')


class SewaForm(fw.FlaskForm):
    pemesan = wt.SelectField('Pemesan', validators=[wt.validators.DataRequired()])
    lokasi_jemput = wt.StringField('Lokasi Jemput', validators=[wt.validators.DataRequired()])
    jemput = wt.DateTimeField(format="%Y-%m-%d %H:%M", validators=[wt.validators.DataRequired()])
    est_tiba = wt.DateTimeField(format="%Y-%m-%d %H:%M")
    booking = wt.SelectField('Mobil')
    mobil = wt.SelectField('Mobil')
    supir = wt.SelectField('Mobil')
    harga = wt.IntegerField('Harga')
    tujuan = wt.StringField('Name')
    keterangan = wt.StringField('Name')
    km_berangkat = wt.IntegerField()
    km_tiba = wt.IntegerField()
    
class BeaForm(fw.FlaskForm):
    bea_supir = wt.IntegerField()
    bea_tol = wt.IntegerField()
    bea_bensin = wt.IntegerField()
    bea_lain = wt.IntegerField()
    
    
@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = SewaForm(kapan=datetime.datetime.now())
    form.pemesan.choices = [(c.id, c.name + ' ' + c.phone) for c in Customer.select().order_by(Customer.name.asc())]
    form.mobil.choices = [(c.id, "{} {} {}".format(c.merk, c.model, c.nopol)) for c in Mobil.select()]
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

