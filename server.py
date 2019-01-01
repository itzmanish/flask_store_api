# importing neccessary library
from flask import Flask, request
from flask_restful import Resource, Api

# initalizing
app = Flask(__name__)
api = Api(app)

# Data initalize as document
Store = [
    {
        'name': 'My Item',
        'price': 15.99
    }
]


# create new resource
class Items(Resource):
    """
    New resource for Item class
    """

    # GET method
    def get(self, name):
        # used lambda function for better code structure
        item = next(filter(lambda x: x['name'] == name, Store), None)
        return {'item': item}, 200 if item else 400

    # POST method
    def post(self, name):
        request_data = request.get_json()
        if next(filter(lambda x: x['name'] == name, Store), None):
            return 'The item {} is already exists. please try another one'.format(name), 400
        item = {'name': name, 'price': request_data['price']}
        Store.append(item)
        return item, 201


class ItemsList(Resource):
    """ 
    Resource for class ItemsList
    """

    # GET request
    def get(self):
        return Store


# route resource and register custom resource to Resource
# this endpoint can be accessed at http://localhost:5000/students/"any name you can type here"
api.add_resource(Items, '/items/<string:name>')

# route for retrieve Items
api.add_resource(ItemsList, '/items')

# run app with debug mode if env is development
if __name__ == "__main__":
    app.run(debug=True)

# else run directly
app.run()
