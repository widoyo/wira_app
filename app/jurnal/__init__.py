import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Jurnal


bp = Blueprint('jurnal', __name__, url_prefix='/jurnal')


class JurnalForm(fw.FlaskForm):
    tanggal = wt.DateField('Tanggal')
    name = wt.StringField('Name')
    phone = wt.StringField('WhatsApp')

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = JurnalForm()
    if form.validate_on_submit():
        new_jurnal = Jurnal(**form.data)
        new_jurnal.save()
        return redirect('/jurnal')
    return render_template('jurnal/add.html', form=form)

@bp.route('/<id>')
def show(id):
    jurnal = get_object_or_404(Jurnal, Jurnal.id==id)
    return render_template('jurnal/show.html', jurnal=jurnal)

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
    return render_template('jurnal/index.html', jurnals=jurnals, start=start, end=end, prev=prev, next=next)

