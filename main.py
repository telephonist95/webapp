from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required
from flask_login import current_user, login_user, logout_user
from data import db_session
from data.user import User
from data.building import Building
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.building_form import BuildingForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask_secret_key'
administrator_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

geocoder_key = "40d1649f-0493-4b70-98ba-98533de7710b"

db_session.global_init("db/db.sqlite")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    buildings = db_sess.query(Building).all()
    return render_template("index.html", title="Выбор корпуса", buildings=buildings, apikey=geocoder_key)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(form.password.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if form.key.data != administrator_key:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверный ключ администратора")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_building',  methods=['GET', 'POST'])
@login_required
def add_building():
    form = BuildingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Building).filter(Building.number == form.number.data).first():
            return render_template('building.html', title='Добавление корпуса',
                                   form=form,
                                   message="Такой корпус уже есть")
        building = Building()
        building.number = form.number.data
        building.address = form.address.data
        building.floors_count = form.floors_count.data
        db_sess.add(building)
        db_sess.commit()
        return redirect('/')
    return render_template('building.html', title='Добавление корпуса', 
                           form=form)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
