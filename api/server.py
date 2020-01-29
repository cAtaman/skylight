import os
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from flask import Flask, request
from sms import course_reg

app = Flask(__name__)

base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, 'sms', 'database')

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'accounts.db')
app.config['SQLALCHEMY_BINDS'] = {'master': 'sqlite:///' + os.path.join(db_path, 'master.db'),
                                  'courses': 'sqlite:///' + os.path.join(db_path, 'courses.db'),
                                  '2003-2004': 'sqlite:///' + os.path.join(db_path, '2003-2004.db'),
                                  '2004-2005': 'sqlite:///' + os.path.join(db_path, '2004-2005.db'),
                                  '2005-2006': 'sqlite:///' + os.path.join(db_path, '2005-2006.db'),
                                  '2006-2007': 'sqlite:///' + os.path.join(db_path, '2006-2007.db'),
                                  '2007-2008': 'sqlite:///' + os.path.join(db_path, '2007-2008.db'),
                                  '2008-2009': 'sqlite:///' + os.path.join(db_path, '2008-2009.db'),
                                  '2009-2010': 'sqlite:///' + os.path.join(db_path, '2009-2010.db'),
                                  '2010-2011': 'sqlite:///' + os.path.join(db_path, '2010-2011.db'),
                                  '2011-2012': 'sqlite:///' + os.path.join(db_path, '2011-2012.db'),
                                  '2012-2013': 'sqlite:///' + os.path.join(db_path, '2012-2013.db'),
                                  '2013-2014': 'sqlite:///' + os.path.join(db_path, '2013-2014.db'),
                                  '2014-2015': 'sqlite:///' + os.path.join(db_path, '2014-2015.db'),
                                  '2015-2016': 'sqlite:///' + os.path.join(db_path, '2015-2016.db'),
                                  '2016-2017': 'sqlite:///' + os.path.join(db_path, '2016-2017.db'),
                                  '2017-2018': 'sqlite:///' + os.path.join(db_path, '2017-2018.db')}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

@app.route('/course_reg')
def crs_reg():
    mat_no = str(request.args.get('mat_no'))
    level = int(request.args.get('level'))
    return course_reg.get(mat_no,level)

@app.route('/')
def hello():
    return "Hello world"