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
from app.models import Mobil, Vendor


bp = Blueprint('mobil', __name__, url_prefix='/mobil')


class MobilForm(fw.FlaskForm):
    nopol = wt.StringField('Nopol')
    merk = wt.StringField('Merk')
    model = wt.StringField('Model')
    vin = wt.StringField('No Rangka')
    warna = wt.StringField('Warna')
    akhir_stnk = wt.DateField('Akhir STNK')
    vendor = wt.SelectField('Pemilik')

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = MobilForm()
    form.vendor.choices = [(v.id, v.name) for v in Vendor.select()]
    #form.vendor.choices.append([(v.id, v.name) for v in Vendor.select()])
    if form.validate_on_submit():
        new_cust = Mobil(**form.data)
        if not form.data['vendor']:
            new_cust.vendor = None
        new_cust.c_by = current_user.username
        new_cust.save()
        return redirect('/mobil')
    return render_template('mobil/add.html', form=form)

@bp.route('/<id>')
def show(id):
    mobil = get_object_or_404(Mobil, Mobil.id==id)
    return render_template('mobil/show.html', mobil=mobil)

@bp.route('')
def index():
    mobils = Mobil.select().order_by(Mobil.id.desc())
    return render_template('mobil/index.html', mobils=mobils)

