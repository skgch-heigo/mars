from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('author', required=True, type=int)

parser2 = reqparse.RequestParser()
parser2.add_argument('team_leader', required=False, type=int)
parser2.add_argument('job', required=False)
parser2.add_argument('work_size', required=False, type=int)
parser2.add_argument('collaborators', required=False)
parser2.add_argument('is_finished', required=False, type=bool)
parser2.add_argument('author', required=False, type=int)
