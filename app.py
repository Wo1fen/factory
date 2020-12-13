from flask import Flask, jsonify, render_template, abort, flash, request, redirect, url_for
from models import Database
from forms import ClientForm, FactoryForm, ProductionForm, PositionForm, OrderForm, WorkshopForm, ReleaseForm, WorkerForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "Hello-world!!!"
db = Database('factory', 'postgres', '123')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/debug')
def debug():
    return jsonify(db.get_worker())

@app.route('/client/')
@app.route('/client/<int:id>', methods=['GET', 'DELETE'])
def client(id=None):
    if not id:
        rows = db.get_client()
        header = ("Наименование", "Адрес", "Телефон", "Последняя часть трека")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('client', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/client/add', methods=['GET', 'POST'])
def client_add():
    form = ClientForm()
    if form.validate_on_submit():
        try:
            db.add_client(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add.html', form=form)

@app.route('/workshop/')
@app.route('/workshop/<int:id>', methods=['GET', 'DELETE'])
def workshop(id=None):
    if not id:
        rows = db.get_workshop()
        func = lambda x: x[:2] + x[4:]
        header = ("Имя", "Адрес", "Менеджер")
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('workshop', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/workshop/add', methods=['GET', 'POST'])
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
    return render_template('add.html', form=form)

@app.route('/factory/')
@app.route('/factory/<int:id>', methods=['GET', 'DELETE'])
def factory(id=None):
    if not id:
        rows = db.get_factory()
        header = ("Адрес",)
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('factory', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/factory/add', methods=['GET', 'POST'])
def factory_add():
    form = FactoryForm()
    if form.validate_on_submit():
        try:
            db.add_factory(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add.html', form=form)

@app.route('/position/')
@app.route('/position/<int:id>', methods=['GET', 'DELETE'])
def position(id=None):
    if not id:
        rows = db.get_position()
        header = ("Зарплата", "Название")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('position', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/position/add', methods=['GET', 'POST'])
def position_add():
    form = PositionForm()
    if form.validate_on_submit():
        try:
            db.add_position(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add.html', form=form)

@app.route('/release/')
@app.route('/release/<int:id>', methods=['GET', 'DELETE'])
def release(id=None):
    if not id:
        rows = db.get_release()
        header = ("Вес", "Дата выпуска", "Число", "Название цеха", "Дата заказа", "Название продукции")
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
            return "Not ready yet", 404

@app.route('/release/add', methods=['GET', 'POST'])
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
            db.add_release(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add.html', form=form)
    pass

@app.route('/order/')
@app.route('/order/<int:id>', methods=['GET', 'DELETE'])
def order(id=None):
    if not id:
        rows = db.get_order()
        func = lambda x: (x[0],) + x[2:]
        header = ("Трек", "Дата заказа", "Клиент", "Телефон")
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('order', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/order/add', methods=['GET', 'POST'])
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
    return render_template('add.html', form=form)

@app.route('/worker/')
@app.route('/worker/<int:id>', methods=['GET', 'DELETE'])
def worker(id=None):
    if not id:
        rows = db.get_worker()
        func = lambda x: x[:2] + x[4:]
        header = ("ФИО", "Дата приема", "Квалификации", "Должность", "Цех")
        return render_template('table.html', rows=rows, header=header, func=func)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('worker', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/worker/add', methods=['GET', 'POST'])
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
    return render_template('add.html', form=form)

@app.route('/production/')
@app.route('/production/<int:id>', methods=['GET', 'DELETE'])
def production(id=None):
    if not id:
        rows = db.get_production()
        header = ("Имя", "Тип", "Цена")
        return render_template('table.html', rows=rows, header=header)
    else:
        if request.method == 'DELETE':
            try:
                db.delete('production', id)
            except Exception as ex:
                return str(ex), 500
            return 'OK', 200
        else:
            return "Not ready yet", 404

@app.route('/production/add', methods=['GET', 'POST'])
def production_add():
    form = ProductionForm()
    if form.validate_on_submit():
        try:
            db.add_production(form.data)
            flash('<p class="alert alert-success">Запись успешно добавлена</p>')
        except Exception as ex:
            flash(f'<p class="alert alert-danger">Возникла проблема при добавлении записи:<br/>{ex}</p>')
    return render_template('add.html', form=form)

if __name__ == "__main__":
    app.run()
