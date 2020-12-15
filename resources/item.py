import sqlite3
from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from model.item import ItemModel
from flask import jsonify


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs to haev a store_id !")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "there is no such a item."}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f" An item with name, {name} is already exist in database"}, 400
        data_request = Item.parser.parse_args()
        updated_item = ItemModel(name, **data_request)
        try:
            updated_item.save_to_db()
        except:
            return {"message": " An error occurred inserting the item"}

        return updated_item.json(), 201

    @jwt_required()
    def put(self, name):
        data_request = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data_request["price"])

        if not item:
            item = ItemModel(name=name, **data_request)

        else:
            item.price = data_request["price"]
        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        data_request = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {"message": "your item was deleted"}
        return {"message": "there is no such a item."}


class ItemList(Resource):
    def get(self):
        '''if you are working in a team that they are using python as well so use list comprehensive '''
        return {"item": [item.json() for item in ItemModel.query.all()]}

        """if you are working in a team that they are using different languages
         it is better to use map and filter instead of list comprehensive"""
        # return {"item": list(map(lambda x: x.json(), ItemModel.query.all()))}
