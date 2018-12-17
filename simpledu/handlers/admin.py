from flask import Blueprint, render_template, url_for, request, flash, redirect
from simpledu.decorators import admin_required
from flask_login import current_user

from simpledu.exts import db
from simpledu.models import Course, User,LiveBean
from simpledu.forms import CourseForm, AddUserForm, LiveUserForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def admin_index():
    return render_template('admin/index.html', current_user=current_user)


@admin.route("/courses/")
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=9,
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)


@admin.route("/zhibo/")
@admin_required
def zhibo():
    page=request.args.get("page",default=1,type=int)
    pagination=LiveBean.query.paginate(
        page=page,
        per_page=9,
        error_out=False
    )
    return render_template('admin/zhibolist.html',pagination=pagination)


@admin.route("/add_zhibo/",methods=["GET","POST"])
@admin_required
def add_zhibo():
    form = LiveUserForm()
    if form.validate_on_submit():
        form.add_live()
        flash("创建成功", 'success')
        return redirect(url_for('admin.zhibo'))
    return render_template('admin/addzhibo.html',form=form)


@admin.route("/courses/create/", methods=["GET", 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash("课程创建成功", 'success')
        return redirect(url_for('.courses'))
    return render_template('admin/create_course.html', form=form)


@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)


@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程 "{}" 删除成功'.format(course.name), 'success')
    return redirect(url_for('admin.courses'))


@admin.route('/users/')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=9,
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


@admin.route('/users/add', methods=["GET", 'POST'])
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        form.add_user()
        flash("课用户创建成功", 'success')
        return redirect(url_for(".users"))
    return render_template('admin/add_user.html', form=form)


@admin.route('/users/<int:user_id>/edit', methods=['GET', "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AddUserForm(obj=user)
    if form.validate_on_submit():
        form.edit_user(user)
        flash("用户编辑成功", 'success')
        return redirect(url_for('.users'))
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/users/<int:user_id>/del')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('.users'))
