import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from flask_login import current_user
from app.models import Jurnal, Kas, KAS_BANK, KAT_BIAYA, Sewa


bp = Blueprint('kas', __name__, url_prefix='/kas')


class KasOutForm(fw.FlaskForm):
    tanggal = wt.DateField('Tanggal')
    sumber = wt.SelectField(choices=KAS_BANK)
    tujuan = wt.SelectField(choices=KAT_BIAYA)
    nilai = wt.StringField('Nilai')
    keterangan = wt.StringField('Keterangan')
    

class KasInForm(fw.FlaskForm):
    tanggal = wt.DateField('Tanggal')
    sumber = wt.SelectField(choices='401 Sewa;402 Pendapatan Lain-lain;403 Koreksi Saldo;'.split(';'))
    tujuan = wt.SelectField(choices=KAS_BANK)
    nilai = wt.StringField('Nilai')
    #sewa = wt.SelectField('Sewa', choices=[(s.id, s.booking.pemesan.name) for s in Sewa.select()])
    keterangan = wt.StringField('Keterangan')

@bp.route('/addout', methods=['POST', 'GET'])
def addout():
    form = KasOutForm(tanggal=datetime.date.today())
    if form.validate_on_submit():
        new_kasout = Jurnal(**form.data)
        new_kasout.c_by = current_user.username
        new_kasout.is_masuk = False
        new_kasout.save()
        return redirect('/kas')
    return render_template('kas/addout.html', form=form)

@bp.route('/addin', methods=['POST', 'GET'])
def addin():
    form = KasInForm(tanggal=datetime.date.today())
    if form.validate_on_submit():
        new_kasin = Jurnal(**form.data)
        new_kasin.c_by = current_user.username
        new_kasin.is_masuk = True
        new_kasin.save()
        return redirect('/kas')
    return render_template('kas/addin.html', form=form)

@bp.route('/<id>')
def show(id):
    kas = get_object_or_404(Kas, Kas.id==id)
    return render_template('kas/show.html', kas=kas)

@bp.route('')
def index():
    bulan = request.args.get('bln') and datetime.datetime.strptime(request.args.get('bln'), '%Y-%m') or datetime.date.today()
    start = bulan.replace(day=1)
    if bulan.month == datetime.date.today().month:
        end = datetime.date.today()
    else:
        end = (bulan.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    jurnals = Jurnal.select().where(Jurnal.tanggal.between(start, end)).order_by(Jurnal.id.desc())
    prev = (start - datetime.timedelta(days=1)).strftime('%Y-%m')
    next = (start + datetime.timedelta(days=32)).strftime('%Y-%m')
    
    return render_template('kas/index.html', kass=jurnals, start=start, end=end, prev=prev, next=next)

