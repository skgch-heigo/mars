from flask import Flask

from data import db_session

from data.beta_code import Jobs, User
from data.departments import Departments


db_session.global_init("db/blogs.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    # app.run()
    Jobs.__repr__ = lambda x: "<Job> " + x.job
    db_sess = db_session.create_session()
    worked = {}
    for job in db_sess.query(Jobs).filter(Jobs.is_finished == 1):
        if job.team_leader not in worked:
            worked[job.team_leader] = job.work_size
        else:
            worked[job.team_leader] += job.work_size
        for i in job.collaborators.split(", "):
            if int(i) != job.team_leader:
                if int(i) not in worked:
                    worked[int(i)] = job.work_size
                else:
                    worked[int(i)] += job.work_size
    dep = db_sess.query(Departments).filter(Departments.id == 1).first()
    for i in dep.members.split(", "):
        if int(i) in worked and worked[int(i)] > 25:
            user = db_sess.query(User).filter(User.id == int(i)).first()
            print(user.name, user.surname)


if __name__ == '__main__':
    main()
