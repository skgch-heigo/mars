from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument("hashed_password", required=True)

parser2 = reqparse.RequestParser()
parser2.add_argument('surname', required=False)
parser2.add_argument('name', required=False)
parser2.add_argument('age', required=False, type=int)
parser2.add_argument('position', required=False)
parser2.add_argument('speciality', required=False)
parser2.add_argument('address', required=False)
parser2.add_argument('email', required=False)
parser2.add_argument("hashed_password", required=False)
