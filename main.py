from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_required
from flask_login import current_user, login_user, logout_user
from data import db_session
from data.user import User
from data.building import Building
from data.floor import Floor
from data.room import Room
from data.item import Item
from data.type import Type
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.building_form import BuildingForm
from forms.floor_form import FloorForm
from forms.room_form import RoomForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/img/'
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
    buildings = [{"address": building.address,
                  "floors_count": building.floors_count,
                  "number": building.number}
                 for building in db_sess.query(Building).all()]
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
        if form.image.data:
            image_data = request.files[form.image.name].read()
            filename = f"static/{form.image.data.filename}"
            with open(filename, 'wb') as file:
                file.write(image_data)
            building.filepath = form.image.data.filename
        db_sess.add(building)
        db_sess.commit()
        return redirect('/')
    return render_template('add_building.html', title='Добавление корпуса', 
                           form=form)


@app.route('/delete_building/<int:number>', methods=['GET', 'POST'])
@login_required
def delete_building(number):
    db_sess = db_session.create_session()
    building = db_sess.query(Building).filter(Building.number == number).delete()
    floors = db_sess.query(Floor).filter(Floor.building_number == number).delete()
    rooms = db_sess.query(Room).filter(Room.building_number == number).delete()
    items = db_sess.query(Item).filter(Item.building_number == number).delete()
    db_sess.commit()
    return redirect('/')


@app.route('/change_building/<int:number>', methods=['GET', 'POST'])
@login_required
def change_building(number):
    form = BuildingForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        building = db_sess.query(Building).filter(Building.number == number).first()
        if building:
            form.number.data = building.number
            form.floors_count.data = building.floors_count
            form.address.data = building.address
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        building = db_sess.query(Building).filter(Building.number == number).first()
        exists = db_sess.query(Building).filter(Building.number == form.number.data).first()
        if building and (not exists or building.number == form.number.data):
            floors = db_sess.query(Floor).filter(Floor.building_number == number).all()
            rooms = db_sess.query(Room).filter(Room.building_number == number).all()
            items = db_sess.query(Item).filter(Item.building_number == number).all()
            building.number = form.number.data
            building.floors_count =  form.floors_count.data
            building.address = form.address.data
            for floor in floors:
                floor.building_number = building.number
            for room in rooms:
                room.building_number = building.number
            for item in items:
                item.building_number = building.number
            if form.image.data:
                if building.filepath and os.path.exists(f"static/{building.filepath}"):
                    os.remove(f"static/{building.filepath}")
                image_data = request.files[form.image.name].read()
                filename = f"static/{form.image.data.filename}"
                with open(filename, 'wb') as file:
                    file.write(image_data)
                building.filepath = form.image.data.filename
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_building.html',
                           title='Редактирование корпуса',
                           form=form)


@app.route('/building/<int:number>')
def building(number):
    db_sess = db_session.create_session()
    building = db_sess.query(Building).filter(Building.number == number).first()
    floors = db_sess.query(Floor).filter(Floor.building_number == number).all()
    return render_template('building.html',
                           title=f'Корпус {number}',
                           building=building,
                           floors=floors)


@app.route('/delete_floor/<int:building_number>/<int:floor_number>')
@login_required
def delete_floor(building_number, floor_number):
    db_sess = db_session.create_session()
    db_sess.query(Floor).filter(Floor.building_number == building_number, Floor.number == floor_number).delete()
    db_sess.query(Room).filter(Room.building_number == building_number, Room.floor_number == floor_number).delete()
    db_sess.query(Item).filter(Item.building_number == building_number, Item.floor_number == floor_number).delete()
    db_sess.commit()
    return redirect(f'/building/{building_number}')


@app.route('/add_floor/<int:building_number>',  methods=['GET', 'POST'])
@login_required
def add_floor(building_number):
    form = FloorForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Floor).filter(Floor.building_number == building_number, Floor.number == form.number.data).first():
            return render_template('add_floor.html', title='Добавление этажа',
                                   form=form,
                                   message="Такой этаж уже есть")
        floor = Floor()
        floor.building_number = building_number
        floor.number = form.number.data
        floor.rooms_count = form.rooms_count.data
        floor.rooms_coords = form.rooms_coords.data
        if form.image.data:
            image_data = request.files[form.image.name].read()
            filename = f"static/{form.image.data.filename}"
            with open(filename, 'wb') as file:
                file.write(image_data)
            floor.filepath = form.image.data.filename
        db_sess.add(floor)
        for room_stats in floor.rooms_coords.split(';'):
            room_number = int(room_stats.split(':')[0])
            room = Room()
            room.building_number = building_number
            room.floor_number = floor.number
            room.number = room_number
            db_sess.add(room)
        db_sess.commit()
        return redirect(f'/building/{building_number}')
    return render_template('add_floor.html', title='Добавление этажа', 
                           form=form)


@app.route('/change_floor/<int:building_number>/<int:number>', methods=['GET', 'POST'])
@login_required
def change_floor(building_number, number):
    form = FloorForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        floor = db_sess.query(Floor).filter(Floor.number == number, Floor.building_number == building_number).first()
        if floor:
            form.number.data = floor.number
            form.rooms_count.data = floor.rooms_count
            form.rooms_coords.data = floor.rooms_coords
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        floor = db_sess.query(Floor).filter(Floor.number == number, Floor.building_number == building_number).first()
        exists = db_sess.query(Floor).filter(Floor.number == form.number.data, Floor.building_number == building_number).first()
        if floor and (not exists or floor.number == form.number.data):
            rooms = db_sess.query(Room).filter(Room.building_number == building_number, Room.floor_number == number).all()
            items = db_sess.query(Item).filter(Item.building_number == building_number, Item.floor_number == number).all()
            floor.number = form.number.data
            floor.rooms_count = form.rooms_count.data
            floor.rooms_coords = form.rooms_coords.data
            for room in rooms:
                room.building_number = floor.number
            for item in items:
                item.building_number = floor.number
            if form.image.data:
                if floor.filepath and os.path.exists(f"static/{floor.filepath}"):
                    os.remove(f"static/{floor.filepath}")
                image_data = request.files[form.image.name].read()
                filename = f"static/{form.image.data.filename}"
                with open(filename, 'wb') as file:
                    file.write(image_data)
                floor.filepath = form.image.data.filename
            db_sess.commit()
            return redirect(f'/building/{building_number}')
        else:
            abort(404)
    return render_template('add_floor.html',
                           title='Редактирование этажа',
                           form=form)


@app.route('/building/<int:building_number>/<int:number>')
def floor(building_number, number):
    db_sess = db_session.create_session()
    building = db_sess.query(Building).filter(Building.number == building_number).first()
    floor = db_sess.query(Floor).filter(Floor.building_number == building_number, Floor.number == number).first()
    rooms = db_sess.query(Room).filter(Room.building_number == building_number, Room.floor_number == number).all()
    return render_template('floor.html',
                           title=f'Этаж {number}',
                           building=building,
                           floor=floor,
                           rooms=rooms)


@app.route('/delete_room/<int:building_number>/<int:floor_number>/<int:room_number>')
@login_required
def delete_room(building_number, floor_number, room_number):
    db_sess = db_session.create_session()
    db_sess.query(Room).filter(Room.building_number == building_number, Room.floor_number == floor_number, Room.number == room_number).delete()
    db_sess.query(Item).filter(Item.building_number == building_number, Item.floor_number == floor_number, Item.room_number == room_number).delete()
    db_sess.commit()
    return redirect(f'/building/{building_number}/{floor_number}')


@app.route('/add_room/<int:building_number>/<int:floor_number>',  methods=['GET', 'POST'])
@login_required
def add_room(building_number, floor_number):
    form = RoomForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Room).filter(Room.building_number == building_number, Room.floor_number == floor_number, Room.number == form.number.data).first():
            return render_template('add_room.html', title='Добавление этажа',
                                   form=form,
                                   message="Такой кабинет уже есть")
        room = Room()
        room.building_number = building_number
        room.floor_number = floor_number
        room.number = form.number.data
        db_sess.add(room)
        db_sess.commit()
        return redirect(f'/building/{building_number}/{floor_number}')
    return render_template('add_room.html', title='Добавление кабинета', 
                           form=form)


@app.route('/change_room/<int:building_number>/<int:floor_number>/<int:room_number>', methods=['GET', 'POST'])
@login_required
def change_room(building_number, floor_number, room_number):
    form = RoomForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        room = db_sess.query(Room).filter(Room.number == room_number, Room.building_number == building_number, Room.floor_number == floor_number).first()
        if room:
            form.number.data = room.number
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        room = db_sess.query(Room).filter(Room.number == room_number, Room.building_number == building_number, Room.floor_number == floor_number).first()
        exists = db_sess.query(Room).filter(Room.number == form.number.data, Room.building_number == building_number, Room.floor_number == floor_number).first()
        if room and (not exists or room.number == form.number.data):
            items = db_sess.query(Item).filter(Item.building_number == building_number, Item.floor_number == floor_number, Item.room_number == room_number).all()
            room.number = form.number.data
            for item in items:
                item.room_number = room.number
            db_sess.commit()
            return redirect(f'/building/{building_number}/{floor_number}')
        else:
            abort(404)
    return render_template('add_room.html',
                           title='Редактирование кабинета',
                           form=form)



@app.route('/building/<int:building_number>/<int:floor_number>/<int:room_number>')
def room(building_number, floor_number, room_number):
    db_sess = db_session.create_session()
    building = db_sess.query(Building).filter(Building.number == building_number).first()
    floor = db_sess.query(Floor).filter(Floor.building_number == building_number, Floor.number == floor_number).first()
    room = db_sess.query(Room).filter(Room.building_number == building_number, Room.floor_number == floor_number, Room.number == room_number).first()
    items = db_sess.query(Item).filter(Item.building_number == building_number, Item.floor_number == floor_number, Item.room_number == room_number).all()
    types = db_sess.query(Type).all()
    types_dict = {
        type.id: type.name
        for type in types
    }
    return render_template('room.html',
                           title=f'Кабинет {room_number}',
                           building=building,
                           floor=floor,
                           room=room,
                           items=items,
                           types=types_dict)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
