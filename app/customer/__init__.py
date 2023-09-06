import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
from playhouse.flask_utils import get_object_or_404
import flask_wtf as fw
import wtforms as wt
from flask_login import current_user
from wtforms.validators import DataRequired
from app.models import Customer


bp = Blueprint('customer', __name__, url_prefix='/customer')


class CustomerForm(fw.FlaskForm):
    name = wt.StringField('Name')
    phone = wt.StringField('WhatsApp')
    addr1 = wt.StringField('Addr1')
    addr2 = wt.StringField('Addr2')
    city = wt.StringField('Kota')

@bp.route('/<id>/edit', methods=['POST', 'GET'])
def edit(id):
    cust = get_object_or_404(Customer, Customer.id==id)
    form = CustomerForm(obj=cust)
    if form.validate_on_submit():
        form.populate_obj(cust)
        cust.c_by = current_user.username
        cust.save()
        return redirect('/customer')
    return render_template('customer/edit.html', form=form, customer=cust)

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = CustomerForm()
    if form.validate_on_submit():
        new_cust = Customer()
        new_cust.c_by = current_user.username
        new_cust.save()
        return redirect('/customer')
    return render_template('customer/add.html', form=form)

@bp.route('/<id>')
def show(id):
    customer = get_object_or_404(Customer, Customer.id==id)
    return render_template('customer/show.html', customer=customer)

@bp.route('')
def index():
    customers = Customer.select().order_by(Customer.name.asc())
    return render_template('customer/index.html', customers=customers)

