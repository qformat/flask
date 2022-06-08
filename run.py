# -*- coding: utf-8 -*-
# created by K brother
import os
from datetime import timedelta
from runjob.views.user import user
from flask import Blueprint, Flask
import configs
from exts import db
from runjob.views.show import show
from runjob.views.api import api
from runjob.views.code import code
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(show)
app.register_blueprint(user)
app.register_blueprint(api)
app.register_blueprint(code)
app.config.from_object(configs)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
db.init_app(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)


