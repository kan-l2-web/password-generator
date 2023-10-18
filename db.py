import sqlite3


class Encrypter:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def check_user_id(self, id):
        result = self.cursor.execute(
            "SELECT id FROM passwords WHERE id = ?", (id,))
        return bool(len(result.fetchall()))

    def add_password(self, password):
        self.cursor.execute(
            "INSERT INTO passwords (password) VALUES (?)", (password, ))
        return self.connection.commit()

    def get_data(self):
        result = self.cursor.execute(
            "SELECT * FROM passwords")
        return result.fetchall()

    def close(self):
        self.connection.close()
