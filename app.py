from flask import Flask, jsonify
from flask_restful import Api
from security import authenticate, identity as identity_function
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from datetime import timedelta
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
# app.config["SECRET_KEY"] = "mysecretekey"
app.secret_key = 'jose'

api = Api(app)

jwt = JWT(app, authenticate, identity_function)


@jwt.auth_response_handler
def customized_resoponse_handler(access_token, identity):
    return jsonify({"access_token": access_token.decode('utf-8'),
                    "user_id": identity.id})




@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({"message": error.description, "code": error.status_code, }), error.status_code


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
