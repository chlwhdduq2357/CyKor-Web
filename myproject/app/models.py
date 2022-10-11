from app import db


##### database configuration #####
# +------------------------------+
# | model 1. user                |
# +----------+-------------------+
# | id       | id of a user      |
# +----------+-------------------+   
# | username | name of a user    |
# +----------+-------------------+
# | password | encrypted         |
# +----------+-------------------+
# +------------------------------+
# | model 2. post                |
# +----------+-------------------+
# | id       | id of a post      |
# +----------+-------------------+
# | userid   | author of a post  |
# +----------+-------------------+
# | title    | title of a post   |
# +----------+-------------------+
# | time     | time created      |
# +----------+-------------------+
# | content  | content of a post |
# +----------+-------------------+

class User(db.Model):
    _id         = db.Column(db.Integer, primary_key = True)
    _username   = db.Column(db.String, nullable = False)
    _password   = db.Column(db.String, nullable = False) # password encrypted

    
class Post(db.Model):
    _id         = db.Column(db.Integer, primary_key = True)
    _userid     = db.Column(db.Integer, db.ForeignKey('user._id'))
    _title      = db.Column(db.String, nullable = False)
    _time       = db.Column(db.DateTime(), nullable  = False)
    _content    = db.Column(db.String, nullable = False)
