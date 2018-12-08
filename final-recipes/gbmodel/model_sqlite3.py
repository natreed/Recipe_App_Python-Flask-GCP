from datetime import date
from .Model import Model
import sqlite3
DB_FILE = 'recipes.db'    # file for our Database

class model(Model):
    def __init__(self):
        """Create a recipes table if it does not exist"""
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from recipes")
        except sqlite3.OperationalError:
            cursor.execute("create table recipes (title text, author text, ingredients text, instructions text)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: title, author, ingredients, instructions
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM recipes")
        return cursor.fetchall()

    def insert(self, title, author, ingredients, instructions):
        """
        Inserts entry into database
        :param title: String
        :param author: String
        :param ingredients: String
        :param instructions: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'title':title, 'author': author, 'ingredients': ingredients, 'instructions': instructions}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into recipes (title, author, ingredients, instructions) "
                       "VALUES (:title, :author, :ingredients, :instructions)", params)

        connection.commit()
        cursor.close()
        return True

