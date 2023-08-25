import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Kas


bp = Blueprint('kas', __name__, url_prefix='/kas')


class KasForm(fw.FlaskForm):
    tanggal = wt.DateField('Tanggal')
    name = wt.StringField('Name')
    phone = wt.StringField('WhatsApp')

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = KasForm()
    if form.validate_on_submit():
        new_cust = Driver(**form.data)
        new_cust.save()
        return redirect('/kas')
    return render_template('kas/add.html', form=form)

@bp.route('/<id>')
def show(id):
    kas = get_object_or_404(Kas, Kas.id==id)
    return render_template('kas/show.html', kas=kas)

@bp.route('')
def index():
    kass = Kas.select().order_by(Kas.id.desc())
    return render_template('kas/index.html', kass=kass)

