from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.beta_code import Jobs, User
from data.job_parser import parser, parser2


class JobsResource(Resource):
    def get(self, user_id):
        abort_if_jobs_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Jobs).get(user_id)
        return jsonify({'jobs': user.to_dict(
            only=("team_leader",
                  "job",
                  "work_size",
                  "collaborators",
                  "start_date",
                  "end_date",
                  "is_finished",
                  "author"))})

    def delete(self, user_id):
        abort_if_jobs_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Jobs).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_jobs_not_found(user_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(user_id)
        if args['team_leader']:
            job.team_leader = args['team_leader']
        if args['job']:
            job.job = args['job']
        if args['work_size']:
            job.work_size = args['work_size']
        if args['collaborators']:
            job.collaborators = args['collaborators']
        if args['is_finished']:
            job.is_finished = args['is_finished']
        if args['author']:
            job.author = args['author']
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=("team_leader",
                  "job",
                  "work_size",
                  "collaborators",
                  "start_date",
                  "end_date",
                  "is_finished",
                  "author")) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs()
        job.team_leader = args['team_leader']
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        job.author = args['author']
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    user = session.query(Jobs).get(jobs_id)
    if not user:
        abort(404, message=f"Job {jobs_id} not found")
