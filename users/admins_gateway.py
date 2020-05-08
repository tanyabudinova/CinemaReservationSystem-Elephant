from db import instance
from .models import AdminModel, UserModel
from .utls import hash_password


class AdminGateway:
    def __init__(self):
        self.model = AdminModel
        self.db = instance

    def add_id_to_table(self, user_id):
        query = '''
            INSERT INTO admins (user_id)
                VALUES (?)
        '''
        self.db.cursor.execute(query, (user_id,))
        self.db.connection.commit()
        admin_query = '''
            SELECT id FROM admins
            ORDER BY id desc LIMIT 1
        '''

        self.db.cursor.execute(admin_query)
        admin_id = self.db.cursor.fetchall()

        return admin_id[0][0]

    def login(self, username, password):
        query = '''
            SELECT * FROM users
            WHERE username == ? and password == ?
        '''
        password = hash_password(password)
        self.db.cursor.execute(query, (username, password))
        user = self.db.cursor.fetchall()

        if len(user) == 0:
            # answer = input('You dont have account yet. Do you want to create one? [y/n]: ')
            # if answer == 'y':
            #     return 'create_account'
            # else:
            #     return 'stop_the_program'
            return False
        self.model.user_id = user[0][0]
        return self.model

    def show_all_admins(self, current_user):
        query = '''
        SELECT user_id, username, password FROM admins
        JOIN users ON admins.user_id = users.id
        '''
        self.db.cursor.execute(query)
        admins = self.db.cursor.fetchall()
        return [UserModel(*admin) for admin in admins]

    def delete_admin(self, number_id):
        delete_from_admin = '''
        DELETE FROM admins
        WHERE user_id == ?
        '''
        self.db.cursor.execute(delete_from_admin, (number_id,))
        delete_from_users = '''
        DELETE FROM users
        WHERE id == ?
        '''
        self.db.cursor.execute(delete_from_users, (number_id,))

        self.db.connection.commit()
        return number_id
