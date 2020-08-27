from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asif'
api = Api(app)

# Create the database using sqlalchemy
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth


# Making the resource accessible via api
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)

# Notes

# JWT - JSON web token. Encodes messages so only those with a particular decryption key can read it.

# Next gives us the first item matched by the filter function
    # If next function doesn't find an item, it returns none
# Filter function has the lambda conditional function as the first arg
    # and the list as the second arg
