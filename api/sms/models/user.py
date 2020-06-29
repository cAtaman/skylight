from sms.config import db, ma


class User(db.Model):
    username = db.Column(db.Text, primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    permissions = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, unique=True, nullable=False)
    fullname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)



class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('password',)
        sqla_session = db.session
