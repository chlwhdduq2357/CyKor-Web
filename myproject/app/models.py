from app import db
from werkzeug.security import generate_password_hash, check_password_hash

##### database configuration #####
# +------------------------------+
# | model 1. user                |
# +----------+-------------------+
# | userid   | id of a user      |
# +----------+-------------------+   
# | username | name of a user    |
# +----------+-------------------+
# | password | encrypted         |
# +----------+-------------------+
# +------------------------------+
# | model 2. post                |
# +----------+-------------------+
# | userid   | id of an author   |
# +----------+-------------------+
# | title    | title of a post   |
# +----------+-------------------+
# | time     | time created      |
# +----------+-------------------+
# | content  | content of a post |
# +----------+-------------------+

class User(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    _userid     = db.Column(db.String, nullable = False)
    _username   = db.Column(db.String, nullable = False)
    _password   = db.Column(db.String, nullable = False)

    def __init__ (self, userid, username, password):
        self._username = username
        self._password = generate_password_hash(password)
        self._userid = userid

    def password_check(self, password):
        return check_password_hash(self.password, password)

    
class Post(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    _userid     = db.Column(db.String, db.ForeignKey('user.id'))
    _title      = db.Column(db.String, nullable = False)
    _time       = db.Column(db.DateTime(), nullable  = False)
    _content    = db.Column(db.String, nullable = False)
