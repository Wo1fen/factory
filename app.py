from flask import Flask, jsonify, render_template, abort, flash, request, redirect, url_for
from models import Database, User
from forms import ClientForm, FactoryForm, ProductionForm, PositionForm, OrderForm, WorkshopForm, ReleaseForm, WorkerForm, LoginForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "Hello-world!!!"
db = Database('factory', 'postgres', '123')
login = LoginManager()
login.init_app(app)
login.login_view = 'login_view'
login.login_message = '<p class="alert alert-warning">Чтобы отобразить эту страницу, пожалуйста, войдите</p>'

@login.user_loader
def load_user(user_id):
    return User.get_user_by_id(db, int(user_id))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_view'))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_name(db, form.username.data)
        if user is None or not user.authenticate(form.password.data):
            flash('<p class="alert alert-warning">Неправильный логин или пароль</p>')
            return redirect(url_for('login_view'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/debug')
def debug():
    return jsonify(db.get_release())

@app.route('/client/')
@app.route('/client/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def client(id=None):
    if not id:
        rows = db.get_client()
        header = ("#", "Наименование", "Адрес", "Телефон", "Последняя часть трека")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('client', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_client(id)
            data = dict(zip(['id', 'name', 'address', 'phone'], row))
            form = ClientForm(data=data)
            if form.validate_on_submit():
                try:
                    db.edit_client(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)

@app.route('/client/add', methods=['GET', 'POST'])
@login_required
def client_add():
    form = ClientForm()
    if form.validate_on_submit():
        try:
            db.add_client(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/workshop/')
@app.route('/workshop/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def workshop(id=None):
    if not id:
        rows = db.get_workshop()
        func = lambda x: x[:2] + x[4:]
        header = ("#", "Имя", "Адрес", "Менеджер")
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('workshop', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_workshop(id)
            data = dict(zip(['id', 'name', 'id_factory', 'id_manager'], row))
            form = WorkshopForm(data=data)
            factories = db.get_factory()
            managers = db.get_worker()
            form.id_factory.choices = [(x[0], x[1]) for x in factories]
            form.id_manager.choices = [(x[0], x[1]) for x in managers]
            if form.validate_on_submit():
                try:
                    db.edit_workshop(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)

@app.route('/workshop/add', methods=['GET', 'POST'])
@login_required
def workshop_add():
    form = WorkshopForm()
    factories = db.get_factory()
    managers = db.get_worker()
    form.id_factory.choices = [(x[0], x[1]) for x in factories]
    form.id_manager.choices = [(x[0], x[1]) for x in managers]
    if form.validate_on_submit():
        try:
            db.add_workshop(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/factory/')
@app.route('/factory/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def factory(id=None):
    if not id:
        rows = db.get_factory()
        header = ("#", "Адрес")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('factory', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_factory(id)
            data = dict(zip(['id', 'address'], row))
            form = FactoryForm(data=data)
            if form.validate_on_submit():
                try:
                    db.edit_factory(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)


@app.route('/factory/add', methods=['GET', 'POST'])
@login_required
def factory_add():
    form = FactoryForm()
    if form.validate_on_submit():
        try:
            db.add_factory(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/position/')
@app.route('/position/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def position(id=None):
    if not id:
        rows = db.get_position()
        header = ("#", "Зарплата", "Название")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('position', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_position(id)
            data = dict(zip(['id', 'salary', 'name'], row))
            form = PositionForm(data=data)
            if form.validate_on_submit():
                try:
                    db.edit_position(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)

@app.route('/position/add', methods=['GET', 'POST'])
@login_required
def position_add():
    form = PositionForm()
    if form.validate_on_submit():
        try:
            db.add_position(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/release/')
@app.route('/release/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def release(id=None):
    if not id:
        rows = db.get_release()
        header = ("#", "Вес", "Дата выпуска", "Число", "Название цеха", "Дата заказа", "Название продукции")
        func = lambda x: x[:3] + (x[4],) + x[7:]
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('release', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_release(id)
            data = dict(zip(['id', 'weight', 'rdate', 'id_workshop', 'count', 'id_production', 'id_order'], row))
            form = ReleaseForm(data=data)
            productions = db.get_production()
            workshops = db.get_workshop()
            orders = db.get_order()
            form.id_production.choices = [(x[0], x[1]) for x in productions]
            form.id_workshop.choices = [(x[0], x[1]) for x in workshops]
            form.id_order.choices = [(x[0], x[2]) for x in orders]
            if form.validate_on_submit():
                try:
                    db.edit_release(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)


@app.route('/release/add', methods=['GET', 'POST'])
@login_required
def release_add():
    form = ReleaseForm()
    productions = db.get_production()
    workshops = db.get_workshop()
    orders = db.get_order()
    form.id_production.choices = [(x[0], x[1]) for x in productions]
    form.id_workshop.choices = [(x[0], x[1]) for x in workshops]
    form.id_order.choices = [(x[0], x[2]) for x in orders]
    if form.validate_on_submit():
        try:
            # form.data['weight'] = float(form.data['weight'])
            # form.data['count'] = int(form.data['count'])
            db.add_release(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/order/')
@app.route('/order/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def order(id=None):
    if not id:
        rows = db.get_order()
        func = lambda x: (x[0],) + x[2:]
        header = ("#", "Трек", "Дата заказа", "Клиент", "Телефон")
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('order', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_order(id)
            data = dict(zip(['id', 'id_client', 'track_number', 'ordate'], row))
            form = OrderForm(data=data)
            clients = db.get_client()
            choices = [(x[0], x[1]) for x in clients]
            form.id_client.choices = choices
            if form.validate_on_submit():
                try:
                    db.edit_order(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)

@app.route('/order/add', methods=['GET', 'POST'])
@login_required
def order_add():
    form = OrderForm()
    clients = db.get_client()
    choices = [(x[0], x[1]) for x in clients]
    form.id_client.choices = choices
    if form.validate_on_submit():
        try:
            db.add_order(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/worker/')
@app.route('/worker/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def worker(id=None):
    if not id:
        func = lambda x: x[:2] + x[4:]
        rows = db.get_worker()
        header = ("#", "ФИО", "Дата приема", "Квалификации", "Должность", "Цех")
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('worker', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_worker(id)
            data = dict(zip(['id', 'name', 'id_workshop', 'id_position', 'hire_date', 'qualification'], row))
            form = WorkerForm(data=data)
            workshops = db.get_workshop()
            positions = db.get_position()
            form.id_workshop.choices = [(x[0], x[1]) for x in workshops]
            form.id_position.choices = [(x[0], x[2]) for x in positions]
            if form.validate_on_submit():
                try:
                    db.edit_worker(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}<br/>{type(ex)}</p>')
            return render_template('add_edit.html', form=form)

@app.route('/worker/add', methods=['GET', 'POST'])
@login_required
def worker_add():
    form = WorkerForm()
    workshops = db.get_workshop()
    positions = db.get_position()
    form.id_workshop.choices = [(x[0], x[1]) for x in workshops]
    form.id_position.choices = [(x[0], x[2]) for x in positions]
    if form.validate_on_submit():
        try:
            db.add_worker(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/production/')
@app.route('/production/<int:id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def production(id=None):
    if not id:
        rows = db.get_production()
        header = ("#", "Имя", "Тип", "Цена")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('production', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            row = db.get_production(id)
            data = dict(zip(['id', 'name', 'type', 'price'], row))
            form = ProductionForm(data=data)
            if form.validate_on_submit():
                try:
                    db.edit_production(form.data)
                    flash('<p class="alert alert-success">Запись успешно изменена</p>')
                except Exception as ex:
                    flash(f'<p class="alert alert-danger">Возникла проблема при изменении записи:<br/>{ex}</p>')
            return render_template('add_edit.html', form=form)

@app.route('/production/add', methods=['GET', 'POST'])
@login_required
def production_add():
    form = ProductionForm()
    if form.validate_on_submit():
        try:
            db.add_production(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add_edit.html', form=form)

@app.route('/logs/', methods=['GET'])
@login_required
def logs():
    rows = db.get_logs()
    header = ('Таблица', 'Время', 'Пользователь', 'Операция')
    return render_template('table.html', rows=rows, header=header, read_only=True)

if __name__ == "__main__":
    app.run()
