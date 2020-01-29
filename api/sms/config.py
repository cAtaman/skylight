import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import Flask

base_dir = os.path.join(os.path.dirname(__file__),'..')
db_path = os.path.join(base_dir, 'sms','database')

app = Flask(__name__)

with app.app_context():
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    bcrypt = Bcrypt(app)
