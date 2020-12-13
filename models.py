import psycopg2

class Database:
    def __init__(self, database, username, password):
        self.connection = psycopg2.connect(database=database, user=username, password=password)
        self.connection.autocommit = True
    
    def _add_query(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)

    def delete(self, tablename, id):
        cursor = self.connection.cursor()
        cursor.execute(f'DELETE FROM {tablename} WHERE ID=%s', (id,))

    def _get_all(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    
    def get_client(self, id=None):
        query = "SELECT * FROM client"
        if not id:
            return self._get_all(query)
        else:
            pass
    
    def get_worker(self, id=None):
        query = "SELECT worker.*, position.name, workshop.name FROM worker JOIN position ON position.id = id_position JOIN workshop ON workshop.id = id_workshop"
        if not id:
            return self._get_all(query)
            # ID    name    id_workshop id_position hire_date   qualification   position.name   workshop.name
        else:
            pass

    def get_factory(self, id=None):
        query = "SELECT * FROM factory"
        if not id:
            return self._get_all(query)
            # ID    address 
        else:
            pass
    
    def get_production(self, id=None):
        query = "SELECT * FROM production"
        if not id:
            return self._get_all(query)
            # ID    name    type    price 
        else:
            pass

    def get_position(self, id=None):
        query = "SELECT * FROM position"
        if not id:
            return self._get_all(query)
            # ID    calary  name
        else:
            pass

    def get_order(self, id=None):
        query = 'SELECT "order".*, client.name, phone FROM "order" JOIN client ON "order".id_client = client.id'
        if not id:
            return self._get_all(query)
            # ID    id_client   track_number    ordate  name    phone
        else:
            pass

    def get_release(self, id=None):
        query = 'SELECT release.*, workshop.name, "order".ordate, production.name FROM release JOIN workshop ON workshop.id = id_workshop JOIN production ON production.id = id_production JOIN "order" ON "order".id = id_order'
        if not id:
            return self._get_all(query)
            # ID    weight  rdate   id_workshop     count   id_production   id_order    workshop.name   order.ordate    production.name
        else:
            pass

    def get_workshop(self, id=None):
        query='SELECT workshop.*, factory.address, worker.name from workshop join factory on factory.id = id_factory join worker on worker.id = id_manager'
        if not id:
            return self._get_all(query)
            # ID    name    id_factory  id_manager  factory.address     manager.name
        else:
            pass
    
    def add_client(self, params):
        query = 'INSERT INTO client(name, address, phone) VALUES (%(name)s, %(address)s, %(phone)s)'
        self._add_query(query, params)

    def add_worker(self, params):
        query = 'INSERT INTO worker(name, id_workshop, id_position, hire_date, qualification) VALUES (%(name)s, %(id_workshop)s, %(id_position)s, %(hire_date)s, %(qualification)s)'
        self._add_query(query, params)

    def add_factory(self, params):
        query = 'INSERT INTO factory(address) VALUES (%(address)s)'
        self._add_query(query, params)

    def add_production(self, params):
        query = 'INSERT INTO production(name, type, price) VALUES (%(name)s, %(type)s, %(price)s)'
        self._add_query(query, params)
    
    def add_position(self, params):
        query = 'INSERT INTO position(salary, name) VALUES (%(salary)s, %(name)s)'
        self._add_query(query, params)

    def add_order(self, params):
        query = 'INSERT INTO "order"(id_client, track_number, ordate) VALUES (%(id_client)s, %(track_number)s, %(ordate)s)'
        self._add_query(query, params)

    def add_release(self, params):
        query = 'INSERT INTO "release"(id_production, weight, rdate, id_workshop, count, id_order) VALUES (%(id_production)s, %(weight)s, %(rdate)s, %(id_workshop)s, %(count)s, %(id_order)s)'
        self._add_query(query, params)

    def add_workshop(self, params):
        query = 'INSERT INTO workshop(name, id_factory, id_manager) VALUES (%(name)s, %(id_factory)s, %(id_manager)s)'
        self._add_query(query, params)
