from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired
from simpledu.models import db, User


class RegistForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message="用户名不能为空"), Length(3, 24, message="用户名长度3-24")])
    email = StringField('邮箱', validators=[DataRequired(message="邮箱不能为空"), Email()])
    password = PasswordField('密码', validators=[DataRequired(message="密码不能为空"), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(message="密码不能为空"), EqualTo('password')])
    submit = SubmitField('提交')

    # 格式是固定的  def validate_fieldname(self, field):
    def validate_username(self, field):
        if not str.isalnum(field.data.strip()):
            raise ValidationError("用户名只能包含数字和英文")
        elif User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")


    def validate_email(self, filed):
        if User.query.filter_by(email=filed.data).first():
            raise ValidationError("邮箱已经存在")

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    # email = StringField('邮箱', validators=[DataRequired("邮箱不能为空"), Email()])
    username = StringField('Username', validators=[DataRequired("用名密码不能为空"), Length(3, 24,message="长度3-24位")])
    password = PasswordField('密码', validators=[DataRequired(message="密码不能为空"), Length(6, 24, message="密码长度6-24位")])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名没注册")


    def validate_password(self, filed):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_pwd(filed.data):
            raise ValidationError("密码不正确")
