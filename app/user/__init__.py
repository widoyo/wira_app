from flask import Blueprint, redirect, render_template
import flask_wtf as fw
from flask_login import current_user
import wtforms as wt
from app.models import User

bp = Blueprint('user', __name__, url_prefix='/user')

class UserForm(fw.FlaskForm):
    username = wt.StringField('Nilai')
    password = wt.StringField('Keterangan')
    role = wt.SelectField('Role', choices=[(0, 'Teknis'), (9, 'AdminKug')])


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = UserForm()
    if form.validate_on_submit():
        new_cust = User(**form.data)
        new_cust.c_by = current_user.username
        new_cust.save()
        return redirect('/user')
    return render_template('user/add.html', form=form)
 
@bp.route('')
def index():
    users = User.select().order_by(User.username.asc())
    return render_template('/user/index.html', users=users)