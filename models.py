from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.Text(20)
                         , primary_key = True
                         , unique = True
                         , nullable = False)
    password = db.Column(db.Text
                         , nullable = False)
    email = db.Column(db.Text(50)
                      , nullable = False
                      , unique = True)
    first_name = db.Column(db.Text(30)
                           , nullable = False)
    last_name = db.Column(db.Text(30)
                          , nullable = False)
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username = username,
            password = hashed_utf8,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False