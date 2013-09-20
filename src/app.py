from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from sqlalchemy import ForeignKey
from sqlalchemy.orm import joinedload, relationship
from sqlalchemy.sql import func
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# Model
db = SQLAlchemy(app)

# association table
link_tag = db.Table('link_tag', db.Model.metadata, db.Column('link_id', db.Integer, ForeignKey('link.id'), nullable=False), db.Column('tag_id', db.Integer, ForeignKey('tag.id'), nullable=False))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    netid = db.Column(db.String(30), nullable=True, unique=True)
    university_id = db.Column(db.String(30), nullable=True, unique=True)
    status = db.Column(db.String(30), nullable=False)
    # FIXME: attempt to fix the presence of user.id in API output
    #links = relationship('Link', backref="user")
    #links = relationship('Link')
    #tags = relationship('Tag')
    created_at = db.Column(db.DateTime(), nullable=False)
    modified_at = db.Column(db.DateTime(), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False) # FIXME: too long for VARCHAR / db.String type?
    title = db.Column(db.String(100), nullable=True)
    annotation = db.Column(db.String(255), nullable=True)
    tags = relationship('Tag', secondary=link_tag, backref='links')
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    modified_at = db.Column(db.DateTime(), nullable=False)
    
    def __repr__(self):
        return '<Link %r>' % self.url
    
    def username(self):
        return db.session.query(User, User.username).filter(User.id == self.user).one().username

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    modified_at = db.Column(db.DateTime(), nullable=False)
    #links = relationship('Link', secondary=link_tag, backref='tags')
    # FIXME: add type (e.g. global, user, course)
    # FIXME: add visibility (e.g. public, internal, private)
    
    def __repr__(self):
        return '<Tag %r>' % self.tag

class IDCard(db.Model):
    __tablename__ = 'idcard'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(30), nullable=False, unique=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    modified_at = db.Column(db.DateTime(), nullable=False)
    
    def __repr__(self):
        return '<IDCard %r>' % self.serial

class APIKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer, primary_key=True)
    apikey = db.Column(db.String(64), nullable=False, unique=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    modified_at = db.Column(db.DateTime(), nullable=False)
    
    def __repr__(self):
        return '<APIKey %r>' % self.apikey
   

# Cross origin request, https://github.com/jfinkels/flask-restless/issues/223
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, GET, POST, PATCH, PUT, OPTIONS, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# API endpoints
# FIXME: change top level from /api to /sim in a single place, if possible
# FIXME: implement API key
manager = APIManager(app, flask_sqlalchemy_db=db)
app.after_request(add_cors_header)
manager.create_api(Link, methods=['GET', 'POST', 'DELETE'], include_methods=['username'], url_prefix='/sim')
manager.create_api(Tag, methods=['GET', 'POST', 'DELETE'], exclude_columns=['links'], url_prefix='/sim')
manager.create_api(User, methods=['GET', 'POST', 'DELETE'], url_prefix='/sim')
manager.create_api(IDCard, methods=['GET', 'POST', 'DELETE'], url_prefix='/sim')
manager.create_api(APIKey, methods=['GET', 'POST', 'DELETE'], url_prefix='/sim')


# Form presentation
@app.route('/link/new')
def link_new():
    return render_template('link_new.html')


# Utilities
def parse_tags(tag_string):
    tag_list = []
    tag_string = re.sub('\s*,\s*', ',', tag_string)
    if (re.search(',', tag_string) == None):
        tag_list.append(tag_string.strip())
    else:
        for tag in re.split(',', tag_string):
            tag_list.append(tag.strip())
    return tag_list


# Form handling
@app.route('/link', methods=['POST'])
def link_create():
    # user autocreation code: disabled
    # user = User(username=request.form['user'],netid=request.form['user'],created_at=func.now(), modified_at=func.now())
    # db.session.add(user)
    # db.session.commit()
    # end user autocreation code
    user = db.session.query(User).filter(User.username == request.form['user']).one()
    
    tags = []
    for t in parse_tags(request.form['tag']):
        # FIXME: filters will also have to include type and visibility
        tag = db.session.query(Tag).filter(Tag.tag == t).filter(Tag.user == user.id).first()
        if (tag == None):  
            tag = Tag(tag=t, user=user.id,created_at=func.now(), modified_at=func.now())
            db.session.add(tag)
        tags.append(tag)
        db.session.commit()
    
    link = Link(url=request.form['url'], user=user.id, tags=tags, annotation=request.form['annotation'], created_at=func.now(), modified_at=func.now())
    db.session.add(link)
    db.session.commit()
    return redirect('/link/new')

if __name__ == '__main__':
    app.debug = True
    app.run()