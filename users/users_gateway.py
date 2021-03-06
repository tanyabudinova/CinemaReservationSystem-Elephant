from db import Database
from .models import UserModel
from .utls import hash_password


class UserGateway:
    def __init__(self):
        self.model = UserModel # To remove
        self.db = Database()

    def create(self, *, username, password):
        if not self.model.validate(username, password):
            return False
        password = hash_password(password)
        query = '''
            INSERT INTO users (username, password)
                VALUES (?, ?)
        '''
        self.db.cursor.execute(query, (username, password))
        self.db.connection.commit()
        user_query = '''
            SELECT *
            FROM users
            ORDER BY id desc
            LIMIT 1
        '''
        self.db.cursor.execute(user_query)
        user_model = self.db.cursor.fetchall()
        self.model.id, self.model.name, self.model.password = user_model[0][0], user_model[0][1], user_model[0][2] # To remove
        return self.model # To use UserModel

    def select_all(self):
        raw_users = self.db.cursor.execute('''SELECT *
                                                FROM users''')

        return [self.model(**row) for row in raw_users]
