from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import  Course, User
from .exts import db
from flask_migrate import Migrate
from flask_login import LoginManager

def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)


# 注册 flask-login 首先需要实例化一个 LoginManager 对象，
# 调用他的 init_app 方法初始化 app，
# 然后需要使用 user_loader 装饰器注册一个函数，
# 用来告诉 flask-login 如何加载用户对象，
# 最后的 login_view 设置的是登录页面的路由
# ，有了它，当用 flask-login 提供的 login_required 装饰器保护一个路由时，
# 如果用户未登录，就会被重定向到 login_view 指定的页面。

def register_flask_login(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_load(id):
        return User.query.get(id)
    #自动重定向
    login_manager.login_view = 'front.login'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_flask_login(app)
    register_blueprints(app)
    return app
