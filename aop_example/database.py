
import sqlite3

class Connection:

    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def begin_transaction(self):
        self.commit()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def create_table(self, table_name):
        # Note: It would be better to create the table automatically using annotations on the class
        # The fields would also need to be annotated with their SQL types
        self.cursor.execute(
            '''
            CREATE TABLE {}(
                hash INTEGER PRIMARY KEY, 
                _Account__id STRING, 
                _Account__balance NUMBER, 
                _Account__is_active BOOLEAN
            )
            '''.format(table_name)
        )
        self.commit()

    def create_row(self, table_name, hash_value):
        self.cursor.execute(
            'INSERT OR IGNORE INTO {}(hash) VALUES(?)'.format(table_name),
            (hash_value,)
        )

    def set_value(self, table_name, hash_value, field_name, field_value):
        self.create_row(table_name, hash_value)
        self.cursor.execute(
            'UPDATE {} SET {} = ? WHERE hash = ?'.format(table_name, field_name),
            (field_value, hash_value)
        )

    def get_value(self, table_name, hash_value, field_name):
        read_cursor = self.db.cursor()
        results = read_cursor.execute(
            'SELECT {} FROM {} WHERE hash = ?'.format(field_name, table_name),
            (hash_value,)
        )
        results = list(results)
        if len(results) == 0:
            raise Exception(f"Did not find object { hash_value } in the database")
        if len(results) > 1:
            raise Exception(f"Found multiple entries for { hash_value } in the database")
        return results[0][0]


IN_MEMORY_DB = Connection(":memory:")
