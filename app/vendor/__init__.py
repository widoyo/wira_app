from flask import Blueprint, render_template, redirect, request
import flask_wtf as fw
import wtforms as wt
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user
from app.models import Vendor


class VendorForm(fw.FlaskForm):
    name = wt.StringField('Name')
    address = wt.StringField('Address')
    pic_name = wt.StringField('PIC Name')
    pic_hp = wt.StringField('PIC HP')

    submit = wt.SubmitField('Add')

bp = Blueprint('vendor', __name__, url_prefix='/vendor')

@bp.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    vendor = get_object_or_404(Vendor, Vendor.id==id)
    form = VendorForm(formdata=request.form, obj=vendor)
    if form.validate_on_submit():
        form.populate_obj(vendor)
        form.save()
        return redirect('/vendor')
    return render_template('vendor/edit.html', form=form, vendor=vendor)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = VendorForm()
    if form.validate_on_submit():
        new_vendor = Vendor(**form.data)
        new_vendor.c_by = current_user.username
        new_vendor.save()
        return redirect('/vendor')
    return render_template('vendor/add.html', form=form)

@bp.route('')
def index():
    vendors = Vendor.select()
    return render_template('vendor/index.html', vendors=vendors)