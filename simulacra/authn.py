import jwt

from flask_login import current_user, login_user
from flask_restless import ProcessingException
from hashlib import sha256
from simulacra.config import config
from simulacra.database import db_session
from simulacra.models import Account
from sqlalchemy.orm.exc import NoResultFound
from time import time

def hash_pass(password=None):
    if password is not None:
        salted_password = password + config.get('secrets', 'SALT')
        return sha256(salted_password).hexdigest()
    else:
        raise ProcessingException(description='Null password in hash_pass', code=500)

def verify_pass(password=None):
    if password is not None:
        if hash_pass(password) == current_user.password:
            return True
    return False

# POST preprocessor for session
def create_session(data=None, **kw):
    if data is not None:
        hashed_pass = hash_pass(data['password'])
        try:
            account = db_session.query(Account).filter(Account.username==data['username']).filter(Account.password==hashed_pass).one()
            data['account_id'] = account.id
        except NoResultFound:
            raise ProcessingException(description='Credentials rejected', code=401)
        del data['username']
        del data['password']

# POST postprocessor for session
def perform_login(result=None, **kw):
    if result is not None:
        print result
        try:
            account = db_session.query(Account).filter(Account.username==result['account']['username']).one()
            login_user(account) #, remember=True)
            token = jwt.encode({'exp': int(time() + 432000), # 5 day session
                                'data': {'username': account.username, 'account_id': account.id, 'session': result['guid']}},
                               config.get('secrets', 'JWT_SECRET'))
            result['token'] = token
            result['account_id'] = account.id
            keys = result.keys()
            for k in keys:
                if k != 'token' and k != 'account_id':
                    del result[k]
        except NoResultFound:
            pass

# preprocessor for any API call that requires authentication
def authn_func(*args, **kw):
    if current_user.is_authenticated():
        # FIXME: check that session exists and is not expired
        pass
    else:
        raise ProcessingException(description='Not authenticated', code=401)
    return True

