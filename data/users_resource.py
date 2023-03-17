from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.beta_code import Jobs, User
from data.user_parser import parser, parser2


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_news_not_found(user_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.name = args['name']
        if args['age']:
            user.age = args['age']
        if args['position']:
            user.position = args['position']
        if args['speciality']:
            user.speciality = args['speciality']
        if args['address']:
            user.address = args['address']
        if args['email']:
            user.email = args['email']
        if args['hashed_password']:
            user.hashed_password = args['hashed_password']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.hashed_password = args['hashed_password']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResourceDemo(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_news_not_found(user_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.name = args['name']
        if args['age']:
            user.age = args['age']
        if args['position']:
            user.position = args['position']
        if args['speciality']:
            user.speciality = args['speciality']
        if args['address']:
            user.address = args['address']
        if args['email']:
            user.email = args['email']
        if args['hashed_password']:
            user.hashed_password = args['hashed_password']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResourceDemo(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.hashed_password = args['hashed_password']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
