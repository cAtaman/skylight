import os
import secrets
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, 'database')

connex_app = connexion.App(__name__, specification_dir=base_dir)
app = connex_app.app

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'accounts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
