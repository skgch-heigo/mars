import json

from flask import Flask, url_for, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo

from data import db_session

from data.beta_code import Jobs, User
from data.departments import Departments

db_session.global_init("db/blogs.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    user1 = StringField('Id астронавта', validators=[DataRequired()])
    pass1 = PasswordField('Пароль астронавта', validators=[DataRequired()])
    user2 = StringField('Id капитана', validators=[DataRequired()])
    pass2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class UserForm(FlaskForm):
    email = EmailField('Email/login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat password', validators=[DataRequired(),
                                                           EqualTo('password',
                                                                   message='Passwords must match')])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form,
                           emblem=url_for('static', filename='img/MARS-2-7.png'))


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/training/<prof>')
def training(prof):
    if "строитель" in prof or "инженер" in prof:
        param = {"url": url_for('static', filename='img/engineer.jpg'), "title": "Инженерные тренажеры"}
    else:
        param = {"url": url_for('static', filename='img/science.jpg'), "title": "Научные симуляторы"}
    return render_template('training.html', **param)


@app.route('/table/<gender>/<age>')
def tabling(gender, age):
    param = {"title": "Цвет каюты"}
    if int(age) < 21:
        param["pic_url"] = url_for('static', filename='img/young_alien.jpg')
    else:
        param["pic_url"] = url_for('static', filename='img/old_alien.jpg')
    if gender == "female":
        if int(age) < 21:
            param["color"] = "#f27979"
        else:
            param["color"] = "#a32929"
    else:
        if int(age) < 21:
            param["color"] = "#79a3f2"
        else:
            param["color"] = "#1c3a70"
    return render_template('tabling.html', **param)


@app.route('/list_prof/<tp>')
def list_prof(tp):
    prof_list = ["инженер-исследователь", "пилот", "строитель", "экзобиолог", "врач",
                 "инженер по терраформированию", "климатолог", "специалист по радиационной защите",
                 "астрогеолог", "гляциолог", "инженер жизнеобеспечения", "метеоролог", "оператор марсохода",
                 "киберинженер", "штурман", "пилот дронов"]
    if tp not in ["ol", "ul"]:
        return """<h1>Ошибка<h1>"""
    return render_template('list_prof.html', tp=tp, prof_list=prof_list)


@app.route('/answer')
@app.route('/auto_answer')
def answers():
    params = {
        "title": "Анкета",
        "surname": "Такойтович",
        "name": "Кто-то",
        "education": "какое-то",
        "profession": "а зачем спрашиваете?",
        "sex": "а кто это спрашивает?",
        "motivation": "а может я не хочу говорить",
        "ready": "False",
        "css_file": url_for('static', filename='css/style.css')
    }
    return render_template('auto_answer.html', **params)


@app.route('/distribution')
def distr():
    params = {
        "title": "Размещение",
        "names": ["Пётр Петрович", "Иван Иванов", "Николай Кузнецов", "Александр 2"],
        "css_file": url_for('static', filename='css/style.css')
    }
    return render_template('distribution.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = UserForm()
    if form.validate_on_submit():
        ans = {"surname": "",
               "name": "",
               "age": "",
               "position": "",
               "speciality": "",
               "address": "",
               "email": "", "password": ""}
        for i in ans:
            if i in request.form:
                ans[i] = request.form[i]
        user = User()
        user.name = ans["name"]
        user.surname = ans["surname"]
        user.email = ans["email"]
        user.position = ans["position"]
        user.speciality = ans["speciality"]
        user.address = ans["address"]
        user.age = ans["age"]
        user.hashed_password = str(hash(ans["password"]))
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return render_template('sent.html')
    return render_template('user_form.html', title='Register', form=form)


@app.route('/jobs')
def jobs():
    jobs_dict = []
    db_sess = db_session.create_session()
    for job in db_sess.query(Jobs):
        jobs_dict.append({"id": job.id, "title": job.job,
                          "leader": None,
                          "duration": str(job.work_size) + " hours",
                          "collabs": job.collaborators,
                          "finish": ("Is finished" if job.is_finished else "Is not finished")})
        user = db_sess.query(User).filter(User.id == job.team_leader).first()
        jobs_dict[-1]["leader"] = user.name + " " + user.surname
    params = {
        "title": "Jobs",
        "jobs": jobs_dict
    }
    return render_template('jobs.html', **params)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/odd_even')
def odd_even():
    return render_template('odd_even.html', number=2)


@app.route('/news')
def news():
    with open("static/json/news.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list)


@app.route('/queue')
def que():
    return render_template('queue.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
