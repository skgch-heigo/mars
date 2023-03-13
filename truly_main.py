import datetime
import json

from flask import Flask, url_for, render_template, redirect, request, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session

from data.beta_code import Jobs, User
from data.departments import Departments
from data.category import Category

from data.forms.login_in import LoginInForm
from data.forms.user import UserForm
from data.forms.job import JobForm
from data.forms.deps import DepsForm

db_session.global_init("db/blogs.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    user1 = StringField('Id астронавта', validators=[DataRequired()])
    pass1 = PasswordField('Пароль астронавта', validators=[DataRequired()])
    user2 = StringField('Id капитана', validators=[DataRequired()])
    pass2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


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


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs()
        db_sess = db_session.create_session()
        job.job = form.title.data
        job.team_leader = int(form.team_leader.data)
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        cats = []
        for i in db_sess.query(Category).filter(Category.id.in_(form.category.data.split(", "))):
            cats.append(i)
        job.categories = cats
        job.is_finished = form.is_finished.data
        job.author = current_user.id
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job_form.html', title='Добавление работы',
                           form=form, action="add", data=None, categories="")


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_dep():
    form = DepsForm()
    if form.validate_on_submit():
        dep = Departments()
        db_sess = db_session.create_session()
        dep.title = form.title.data
        dep.chief = int(form.chief.data)
        dep.members = form.members.data
        dep.email = form.email.data
        dep.author = current_user.id
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('deps.html', title='Добавление департамента',
                           form=form, action="add", data=None)


@app.route('/delete_department/<id_dep>')
@login_required
def delete_dep(id_dep):
    db_sess = db_session.create_session()
    data = db_sess.query(Departments).filter(Departments.id == id_dep).first()
    if current_user.id == 1 or current_user.id == data.chief:
        db_sess.delete(data)
        db_sess.commit()
        return redirect('/departments')
    return "У вас нет прав на это действие"


@app.route('/delete_job/<id_job>')
@login_required
def delete_job(id_job):
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    if data.author == current_user.id or current_user.id == 1 or current_user.id == data.team_leader:
        db_sess.delete(data)
        db_sess.commit()
        return redirect('/')
    return "У вас нет прав на это действие"


@app.route('/change_department/<id_dep>', methods=['GET', 'POST'])
@login_required
def change_dep(id_dep):
    db_sess = db_session.create_session()
    data = db_sess.query(Departments).filter(Departments.id == id_dep).first()
    if current_user.id == 1 or current_user.id == data.chief:
        form = DepsForm()
        if form.validate_on_submit():
            data.title = form.title.data
            data.chief = int(form.chief.data)
            data.members = form.members.data
            data.email = form.email.data
            data.author = current_user.id
            db_sess.commit()
            return redirect('/departments')
        return render_template('deps.html', title='Изменение департамента',
                               form=form, action="change", data=data)
    return "У вас нет прав на это действие"


@app.route('/change_job/<id_job>', methods=['GET', 'POST'])
@login_required
def change_job(id_job):
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    if data.author == current_user.id or current_user.id == 1 or current_user.id == data.team_leader:
        form = JobForm()
        if form.validate_on_submit():
            data.job = form.title.data
            data.team_leader = int(form.team_leader.data)
            data.work_size = int(form.work_size.data)
            data.collaborators = form.collaborators.data
            cats = []
            for i in db_sess.query(Category).filter(Category.id.in_(form.category.data.split(", "))):
                cats.append(i)
            data.categories = cats
            data.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        return render_template('job_form.html', title='Изменение работы',
                               form=form, action="change", data=data,
                               categories=", ".join([str(i.id) for i in data.categories]))
    return "У вас нет прав на это действие"


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
                          "leader": None, "team_leader": job.team_leader,
                          "duration": str(job.work_size) + " hours",
                          "collabs": job.collaborators, "categories": ", ".join([i.name for i in job.categories]),
                          "finish": ("Is finished" if job.is_finished else "Is not finished")})
        user = db_sess.query(User).filter(User.id == job.team_leader).first()
        jobs_dict[-1]["leader"] = user.name + " " + user.surname
    params = {
        "title": "Jobs",
        "jobs": jobs_dict
    }
    return render_template('jobs.html', **params)


@app.route('/departments')
def deps():
    jobs_dict = []
    db_sess = db_session.create_session()
    for dep in db_sess.query(Departments):
        jobs_dict.append({"id": dep.id, "title": dep.title,
                          "chief": None, "chief_id": dep.chief,
                          "members": dep.members,
                          "email": dep.email})
        user = db_sess.query(User).filter(User.id == dep.chief).first()
        jobs_dict[-1]["chief"] = user.name + " " + user.surname
    params = {
        "title": "Departments",
        "departments": jobs_dict
    }
    return render_template('show_deps.html', **params)


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
