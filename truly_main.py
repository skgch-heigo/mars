import datetime
import json
import hashlib

from flask import Flask, url_for, render_template, redirect, request, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo
from flask_login import LoginManager, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session

from data.beta_code import Jobs, User
from data.departments import Departments

hasher = hashlib.blake2b(key=b'pseudorandom key', digest_size=16)

db_session.global_init("db/blogs.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


# def hash_f(string):
#     ans = 0
#     p = 356
#     m =
#     for i in range(len(string)):
#         ans +=


login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    user1 = StringField('Id астронавта', validators=[DataRequired()])
    pass1 = PasswordField('Пароль астронавта', validators=[DataRequired()])
    user2 = StringField('Id капитана', validators=[DataRequired()])
    pass2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class LoginInForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginInForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(form.password.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_in.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    # return render_template('base.html')
    return redirect("/jobs")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/training/<prof>')
def training(prof):
    if "строитель" in prof or "инженер" in prof:
        param = {"url": url_for('static', filename='img/engineer.jpg'), "title": "Инженерные тренажеры"}
    else:
        param = {"url": url_for('static', filename='img/science.jpg'), "title": "Научные симуляторы"}
    return render_template('training.html', **param)


@app.route("/session_test")
def session_test():
    session.permanent = True
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


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
        # hasher.update(bytes(ans["password"], "utf-8"))
        user.hashed_password = generate_password_hash(ans["password"])
        print([ans["password"]], user.hashed_password, generate_password_hash(ans["password"]))
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
