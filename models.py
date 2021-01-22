import psycopg2
from flask_login import UserMixin
from hashlib import md5

class Database:
    def __init__(self, database, username, password):
        self.connection = psycopg2.connect(database=database, user=username, password=password)
        self.connection.autocommit = True
    
    def _add_edit_query(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)

    def delete(self, tablename, id):
        cursor = self.connection.cursor()
        cursor.execute(f'DELETE FROM {tablename} WHERE ID=%s', (id,))

    def _get(self, query, id=None):
        cursor = self.connection.cursor()
        if id:
            cursor.execute(query + " WHERE ID=%s", (id,))
            row = cursor.fetchone()
            return row
        else:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def get_client(self, id=None):
        # query = "SELECT * FROM client"
        query = "SELECT * FROM get_client"
        return self._get(query, id)
    
    def get_worker(self, id=None):
        # query = "SELECT worker.*, position.name, workshop.name FROM worker JOIN position ON position.id = id_position JOIN workshop ON workshop.id = id_workshop"
        query = "SELECT * FROM get_worker"
        return self._get(query, id)
            # ID    name    id_workshop id_position hire_date   qualification   position.name   workshop.name

    def get_factory(self, id=None):
        # query = "SELECT * FROM factory"
        query = "SELECT * FROM get_factory"
        return self._get(query, id)
            # ID    address 
    
    def get_production(self, id=None):
        # query = "SELECT * FROM production"
        query = "SELECT * FROM get_production"
        return self._get(query, id)
            # ID    name    type    price 

    def get_position(self, id=None):
        # query = "SELECT * FROM position"
        query = "SELECT * FROM get_position"
        return self._get(query, id)
            # ID    salary  name
    def get_order(self, id=None):
        # query = 'SELECT "order".*, client.name, phone FROM "order" JOIN client ON "order".id_client = client.id'
        query = "SELECT * FROM get_order"
        return self._get(query, id)
            # ID    id_client   track_number    ordate  name    phone

    def get_release(self, id=None):
        #query = 'SELECT release.*, workshop.name, "order".ordate, production.name FROM release JOIN workshop ON workshop.id = id_workshop JOIN production ON production.id = id_production JOIN "order" ON "order".id = id_order'
        query = "SELECT * FROM get_release"
        return self._get(query, id)
            # ID    weight  rdate   id_workshop     count   id_production   id_order    workshop.name   order.ordate    production.name

    def get_workshop(self, id=None):
        #query='SELECT workshop.*, factory.address, worker.name from workshop join factory on factory.id = id_factory join worker on worker.id = id_manager'
        query = "SELECT * FROM get_workshop"
        return self._get(query, id)
            # ID    name    id_factory  id_manager  factory.address     manager.name
    
    def add_client(self, params):
        # query = 'INSERT INTO client(name, address, phone) VALUES (%(name)s, %(address)s, %(phone)s)'
        query = 'CALL add_client(%(name)s, %(address)s, %(phone)s)'
        self._add_edit_query(query, params)

    def add_worker(self, params):
        # query = 'INSERT INTO worker(name, id_workshop, id_position, hire_date, qualification) VALUES (%(name)s, %(id_workshop)s, %(id_position)s, %(hire_date)s, %(qualification)s)'
        query = 'CALL add_worker(%(name)s, %(id_workshop)s, %(id_position)s, %(hire_date)s, %(qualification)s);'
        self._add_edit_query(query, params)

    def add_factory(self, params):
        # query = 'INSERT INTO factory(address) VALUES (%(address)s)'
        query = 'CALL add_factory(%(address)s)'
        self._add_edit_query(query, params)

    def add_production(self, params):
        # query = 'INSERT INTO production(name, type, price) VALUES (%(name)s, %(type)s, %(price)s)'
        query = 'CALL add_production(%(name)s, %(type)s, %(price)s)'
        self._add_edit_query(query, params)
    
    def add_position(self, params):
        # query = 'INSERT INTO position(salary, name) VALUES (%(salary)s, %(name)s)'
        query = 'CALL add_position(%(salary)s, %(name)s)'
        self._add_edit_query(query, params)

    def add_order(self, params):
        # query = 'INSERT INTO "order"(id_client, track_number, ordate) VALUES (%(id_client)s, %(track_number)s, %(ordate)s)'
        query = 'CALL add_order(%(id_client)s, %(track_number)s, %(ordate)s)'
        self._add_edit_query(query, params)

    def add_release(self, params):
        # query = 'INSERT INTO "release"(id_production, weight, rdate, id_workshop, count, id_order) VALUES (%(id_production)s, %(weight)s, %(rdate)s, %(id_workshop)s, %(count)s, %(id_order)s)'
        query = 'CALL public.add_release(%(weight)s::double precision, %(rdate)s, %(id_workshop)s, %(count)s::integer, %(id_production)s, %(id_order)s)'
        self._add_edit_query(query, params)

    def add_workshop(self, params):
        # query = 'INSERT INTO workshop(name, id_factory, id_manager) VALUES (%(name)s, %(id_factory)s, %(id_manager)s)'
        query = 'CALL add_workshop(%(name)s, %(id_factory)s, %(id_manager)s)'
        self._add_edit_query(query, params)

    def edit_client(self, params):
        # query = 'UPDATE client SET name=%(name)s, address=%(address)s, phone=%(phone)s WHERE ID=%(id)s'
        query = 'CALL edit_client(%(id)s, %(name)s, %(phone)s, %(address)s)'
        self._add_edit_query(query, params)
    
    def edit_factory(self, params):
        # query = 'UPDATE factory SET address=%(address)s WHERE ID=%(id)s'
        query = 'CALL edit_factory(%(id)s, %(address)s)'
        self._add_edit_query(query, params)
    
    def edit_production(self, params):
        # query = 'UPDATE production SET name=%(name)s, type=%(type)s, price=%(price)s WHERE ID=%(id)s'
        query = 'CALL edit_production(%(id)s, %(name)s, %(type)s, %(price)s)'
        self._add_edit_query(query, params)
    
    def edit_position(self, params):
        # query = 'UPDATE position SET salary=%(salary)s, name=%(name)s WHERE ID=%(id)s'
        query = 'CALL edit_position(%(id)s, %(salary)s, %(name)s)'
        self._add_edit_query(query, params)
    
    def edit_release(self, params):
        # query = 'UPDATE "release" SET id_production=%(id_production)s, weight=%(weight)s, rdate=%(rdate)s, id_workshop=%(id_workshop)s, count=%(count)s, id_order=%(id_order)s WHERE ID=%(id)s'
        query = 'CALL edit_release(%(id)s, %(weight)s::double precision, %(rdate)s, %(id_workshop)s, %(count)s::integer, %(id_production)s, %(id_order)s)'
        self._add_edit_query(query, params)

    def edit_order(self, params):
        # query = 'UPDATE "order" SET id_client=%(id_client)s, track_number=%(track_number)s, ordate=%(ordate)s WHERE ID=%(id)s'
        query = 'CALL edit_order(%(id)s, %(id_client)s, %(track_number)s, %(ordate)s)'
        self._add_edit_query(query, params)

    def edit_worker(self, params):
        # query = 'UPDATE worker SET name=%(name)s, id_workshop=%(id_workshop)s, id_position=%(id_position)s, hire_date=%(hire_date)s, qualification=%(qualification)s WHERE ID=%(id)s'
        query = 'CALL edit_worker(%(id)s, %(name)s, %(id_workshop)s, %(id_position)s, %(hire_date)s, %(qualification)s)'
        self._add_edit_query(query, params)

    def edit_workshop(self, params):
        # query = 'UPDATE workshop SET name=%(name)s, id_factory=%(id_factory)s, id_manager=%(id_manager)s WHERE ID=%(id)s'
        query = 'CALL edit_workshop(%(id)s, %(name)s, %(id_factory)s, %(id_manager)s)'
        self._add_edit_query(query, params)
    
    def get_logs(self):
        query = 'SELECT * FROM get_logs'
        return self._get(query)

    def get_user_by_name(self, username):
        query = 'SELECT * FROM users WHERE username=%s'
        cursor = self.connection.cursor()
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        return row
    
    def get_user_by_id(self, id):
        query = 'SELECT * FROM users WHERE id_worker=%s'
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        return row

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_user_by_id(db, id):
        row = db.get_user_by_id(id)
        if row:
            return User(int(row[0]), row[1], row[2])
        return None

    @staticmethod
    def get_user_by_name(db, username):
        row = db.get_user_by_name(username)
        if row:
            return User(int(row[0]), row[1], row[2])
        return None
    
    def authenticate(self, password):
        password = md5(bytes(password, encoding="utf-8")).hexdigest()
        if self.password == password:
            return True
        return False
    
    def __str__(self):
        return f"<User: {self.username}>"
