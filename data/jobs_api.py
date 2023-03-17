import flask
from flask import jsonify, make_response, request


from . import db_session
from .beta_code import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=("id",
                                    "team_leader",
                                    "job",
                                    "work_size",
                                    "collaborators",
                                    "start_date",
                                    "end_date",
                                    "is_finished",
                                    "author"))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                "id",
                "team_leader",
                "job",
                "work_size",
                "collaborators",
                "start_date",
                "end_date",
                "is_finished",
                "author"))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["team_leader",
                  "job",
                  "work_size",
                  "collaborators",
                  "is_finished",
                  "author"]):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = Jobs()
    if "id" in request.json:
        if db_sess.query(Jobs).get(request.json["id"]):
            return jsonify({'error': 'Id already exists'})
    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    job.author = request.json['author']
    if "start_date" in request.json:
        job.start_date = request.json["start_date"]
    if "end_date" in request.json:
        job.start_date = request.json["end_date"]
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_news(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs).get(jobs_id)
    if not data:
        return jsonify({'error': 'Id not found'})

    if "team_leader" in request.json:
        data.team_leader = request.json['team_leader']
    if "job" in request.json:
        data.job = request.json['job']
    if "work_size" in request.json:
        data.work_size = request.json['work_size']
    if "collaborators" in request.json:
        data.collaborators = request.json['collaborators']
    if "is_finished" in request.json:
        data.is_finished = request.json['is_finished']
    if "author" in request.json:
        data.author = request.json['author']
    if "start_date" in request.json:
        data.start_date = request.json["start_date"]
    if "end_date" in request.json:
        data.start_date = request.json["end_date"]

    db_sess.commit()
    return jsonify({'success': 'OK'})
