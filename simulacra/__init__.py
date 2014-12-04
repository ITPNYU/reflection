import jwt

from flask import Flask
from flask_login import LoginManager, current_user
from flask_restless import APIManager, ProcessingException
from re import sub
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from simulacra.authn import authn_func, create_session, perform_login
from simulacra.config import config
from simulacra.database import Base, db_session, engine
from simulacra.models import Account, Affiliation, Course, Doc, Person, Project, Section, Session, Subject, Tag, Term, Venue

app = Flask(__name__)
app.secret_key = config.get('secrets', 'SECRET')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong' # or 'basic'

@login_manager.user_loader
def load_account(account_id):
    return db_session.query(Account).get(int(account_id))

@login_manager.request_loader
def load_account_from_request(request):
    authz_header = request.headers.get('Authorization')
    #print('authz_header is ' + str(authz_header))
    if authz_header is not None:
        bearer_token = sub(r'^Bearer ', '', authz_header)
        try:
            bearer_jwt = jwt.decode(bearer_token, config.get('secrets', 'JWT_SECRET'))
            try:
                account = db_session.query(Account).get(bearer_jwt['data']['account_id'])
                if account is not None:
                    return account
            except (MultipleResultsFound, NoResultFound):
                pass
        except (jwt.DecodeError):
            pass
        except (jwt.ExpiredSignature):
            try:
                bearer_jwt = jwt.decode(bearer_token, config.get('secrets', 'JWT_SECRET'), verify_expiration=False)
                session = db_session.query(Session).filter_by(guid=bearer_jwt['data']['session']).one()
                # NOTE: periodically scrub old sessions?
                db_session.delete(session)
            except (jwt.DecodeError, NoResultFound):
                pass
    return None

# Flask-Restless API endpoints
manager = APIManager(
    app, session=db_session,
    preprocessors=dict(
        DELETE=[authn_func],
        GET_SINGLE=[authn_func], GET_MANY=[authn_func],
        PATCH=[authn_func]))
account_blueprint = manager.create_api(
    Account,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='account',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]),
    exclude_columns=['dir_authn', 'password', 'sessions'])
affiliation_blueprint = manager.create_api(
    Affiliation,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='affiliation',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
course_blueprint = manager.create_api(
    Course,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='course',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
doc_blueprint = manager.create_api(
    Doc,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='doc',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
person_blueprint = manager.create_api(
    Person,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='person',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
project_blueprint = manager.create_api(
    Project,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='project',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
section_blueprint = manager.create_api(
    Section,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='section',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
session_blueprint = manager.create_api(
    Session, methods=['POST'],
    collection_name='session',
    url_prefix='/v1',
    preprocessors=dict(POST=[create_session]),
    postprocessors=dict(POST=[perform_login]))
subject_blueprint = manager.create_api(
    Subject,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='subject',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
tag_blueprint = manager.create_api(
    Tag,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='tag',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
term_blueprint = manager.create_api(
    Term,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='term',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))
venue_blueprint = manager.create_api(
    Venue,
    methods=['GET', 'PATCH', 'POST'],
    collection_name='venue',
    url_prefix='/v1',
    max_results_per_page=100,
    preprocessors=dict(POST=[authn_func]))

# Allow API to be accessed from anywhere
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, GET, POST, PATCH, PUT, OPTIONS, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
#    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

app.after_request(add_cors_header)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()