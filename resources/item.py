from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank'
    )

    parser.add_argument('store_id',
        type = int,
        required = True,
        help = 'Every item needs a store id'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item: 
            return item.json()
        return {"message": "Item not found"}, 400 

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{name}' already exists". format(name=name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # Internal Server Error

        return item.json(), 201

        #First we want to ensure that there is no item with the same name.    

        # data = request.get_json(force=True)
        # force=True means you do not need the Content-Type Header. 
        # It will just look  in the content and it will format it even if it is not set.
        # It is nice, but dangerous, because without it you look at it and if it's not correct
        #  it don't do anything, but with it (force=True), you will always do the process even if its not correct
        # 
        # data = request.get_json(silent=True)
        # If there is an error,it will return NONE.
        
        # We no longer need jsonify to return a json,
        # becasue Flask Restful does it for us  

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item deleted"}


    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            # item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}

