from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from models.item import ItemModel

items = []

# Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        payload = Item.parser.parse_args() # -> Error first approach

        item = ItemModel(name, payload['price'], payload['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    @jwt_required
    def put(self, name):
        payload = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            try:
                item = ItemModel(name, **payload) # **payload = payload['price'], payload['store_id']
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            item.price = payload['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        return {'items': [item.json() for item in ItemModel.find_all()]} # Returns all of the objects in the database
        