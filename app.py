from flask import Flask, request
from flask_restful import Resource, Api


# Initializing flask and api with the flask instance
app = Flask(__name__)
api = Api(app)
items = []


class Item(Resource):

    def get(self, name):
        item = next(filter(lambda x: name == x['name'], items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: name == x['name'], items), None):
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}, 200

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: name == x['name'], items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item, 200


class ItemList(Resource):

    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)

