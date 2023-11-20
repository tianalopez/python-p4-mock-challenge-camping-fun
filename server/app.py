#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)


@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers = Camper.query.all()
        dict_campers = [
            {
                'id': camper.id,
                'name': camper.name,
                'age': camper.age
            }
            for camper in campers
        ]
        return dict_campers, 200

    def post(self):
        try:
            data = request.get_json()
            camper = Camper(**data)
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return { "errors": ["validation errors"] }, 400

api.add_resource(Campers, "/campers")

class CampersById(Resource):
    def get(self, id):
        if camper:= db.session.get(Camper, id):
            return camper.to_dict(), 200
        else:
            return {'error': 'Camper not found'}, 404

    def patch(self, id):
        camper = db.session.get(Camper, id)
        if camper:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(camper, attr, data[attr])
                db.session.add(camper)
                db.session.commit()

                dict_camper = {
                    'id': camper.id,
                    'name': camper.name,
                    'age': camper.age
                    }

                return dict_camper, 202
            except:
                db.session.rollback()
                return { "errors": ["validation errors"] }, 400
        else:
            return {'error': 'Camper not found'}, 404
api.add_resource(CampersById, "/campers/<int:id>")

class Activities(Resource):
    def get(self):
        activities = Activity.query.all()
        dict_activities = [
            {
                'id': activity.id,
                'name': activity.name,
                'difficulty': activity.difficulty
            }
            for activity in activities
        ]
        return dict_activities, 200
api.add_resource(Activities, "/activities")

class ActivitiesById(Resource):
    def delete(self, id):
        activity = db.session.get(Activity, id)
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return {}, 204
        else:
            db.session.rollback()
            return {"error": "Activity not found"}, 404
api.add_resource(ActivitiesById, "/activities/<int:id>")

class Signups(Resource):
    def post(self):
        try:
            data = request.get_json()
            signup = Signup(**data)
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(), 201
        except:
            return { "errors": ["validation errors"] }, 400
api.add_resource(Signups, "/signups")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
