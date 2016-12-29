from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
from mongoengine import *

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name",type =str, location ="json")
parser.add_argument("desc",type=str,location ="json")
parser.add_argument("img",type=str,location ="json")

connect(
    'thanhku',
   username = '8f8f8f8',
   password = '123456',
   host = 'ds135798.mlab.com',
   port = 35798
)

class Zodiac(Document):
    name =StringField()
    desc =StringField()
    img = StringField()

nhanma = Zodiac(name= "Nhân mã", desc="Phởn, ham chơi, sợ trách nhiệm",img="http://img.v3.news.zdn.vn/w660/Uploaded/jaroin/2015_12_30/2_1.jpg")

@app.route('/')
def hello_world():
    return 'Hello World!'

def melist2json(list):
    return [json.loads(item.to_json()) for item in list]

class HListRes(Resource):
    def get(self):
        return melist2json(Zodiac.objects)

    def post(self):
        args = parser.parse_args()
        name = args["name"]
        desc = args["desc"]
        img = args["img"]
        print(name,desc,img)
        zodiac= Zodiac(name=name, desc= desc, img=img)
        zodiac.save()
        return json.loads(zodiac.to_json()), 200

class HrcRes(Resource):
    def get(self, hrc_id):
        all_zodiacs= Zodiac.objects
        found_zodiac = all_zodiacs.with_id(hrc_id)
        return json.loads(found_zodiac.to_json())

    def delete(self, hrc_id):
        all_zodiacs = Zodiac.objects
        found_zodiac =  all_zodiacs.with_id(hrc_id)
        found_zodiac.delete()
        return {"code": 1, "status": "OK"}

    def put(self, hrc_id):
        args = parser.parse_args()
        name = args["name"]
        desc = args["desc"]
        img = args["img"]
        all_zodiacs = Zodiac.objects
        found_zodiac = all_zodiacs.with_id(hrc_id)
        found_zodiac.update(set__name=name, set__desc=desc, set__img=img)
        return json.loads(found_zodiac.to_json())

api.add_resource(HListRes,"/api/hrc/")
api.add_resource(HrcRes,"/api/hrc/<hrc_id>")


if __name__ == '__main__':
    app.run()
