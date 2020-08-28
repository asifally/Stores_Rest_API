import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

from db import db



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') # Uses the Heroku env variable else sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'asif' # or app.config['JWT_SECRET_KEY] -> more secure
api = Api(app)

jwt = JWTManager(app) # /auth

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: 
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': "Signature verification failed",
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def unathorized_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def not_fresh_token_callback():
    return jsonify({
        'description': 'Token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.token_in_blacklist_loader
def check_if_in_token_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


# Making the resource accessible via api
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)

# Notes

# JWT - JSON web token. Encodes messages so only those with a particular decryption key can read it.

# Next gives us the first item matched by the filter function
    # If next function doesn't find an item, it returns none
# Filter function has the lambda conditional function as the first arg
    # and the list as the second arg
