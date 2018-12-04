from flask import Blueprint, render_template, request, flash, redirect, url_for, g

from simpledu.config import PAGE_SIZE
from simpledu.models import Course, User
from simpledu.forms import LoginForm, RegistForm
from flask_login import login_user, login_required, logout_user

front = Blueprint('front', __name__)


@front.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=PAGE_SIZE,
        error_out=False
    )
    #courses = Course.query.all()
    return render_template('index.html', pagination=pagination)


@front.route('/login/', methods=["GET", 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, form.remember_me.data)
        flash("登录成功欢迎:" + user.username, 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/register/', methods=["GET", 'POST'])
def register():
    form = RegistForm(request.form)
    if form.validate_on_submit():
        form.create_user()
        flash("注册成功，请登陆", 'success')
        return redirect(url_for('front.login'))
    return render_template('regist.html', form=form)


@front.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("您已经退出登录", 'success')
    return redirect(url_for('.index'))
