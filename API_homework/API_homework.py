from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import mongoengine
from mongoengine import *

host = "ds139278.mlab.com"
port = 39278
db_name = "trangdatabase"
user_name = "DoTrang"
password = "12345678"
mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

parser = reqparse.RequestParser()
parser.add_argument("name",type =str, location ="json")
parser.add_argument("picture",type=str,location ="json")
parser.add_argument("WebLink",type=str,location ="json")


app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


class place(Document):
    name = StringField()
    picture = StringField()
    WebLink = StringField()


def list2json(list):
    return [json.loads(item.to_json()) for item in list]

class PlaceListRes(Resource):
    def get(self):
        return list2json(place.objects)

    def post(self):
        args = parser.parse_args()
        name = args["name"]
        picture = args["picture"]
        WEbLink = args["WebLink"]
        placePost= place(name=name, picture=picture, WebLink=WEbLink)
        placePost.save()
        return json.loads(placePost.to_json()), 200

class PlaceRes(Resource):
    def get(self, hrc_id):
        Place_list= place.objects
        placeGot = Place_list.with_id(hrc_id)
        return json.loads(placeGot.to_json())

    def delete(self, hrc_id):
        Place_list = place.objects
        placeDeleted =  Place_list.with_id(hrc_id)
        placeDeleted.delete()
        return {"code": 1, "status": "OK"}

    def put(self, hrc_id):
        args = parser.parse_args()
        name = args["name"]
        desc = args["desc"]
        img = args["img"]
        Place_list = place.objects
        found_place = Place_list.with_id(hrc_id)
        found_place.update(set__name=name, set__desc=desc, set__img=img)
        return json.loads(found_place.to_json())

api.add_resource(PlaceListRes,"/api/place/")
api.add_resource(PlaceRes,"/api/place/<place_id>")



if __name__ == '__main__':
    app.run()
