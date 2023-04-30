from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb = 'users_schema'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def is_valid_user(user):
        is_valid = True
        if len(user["first_name"]) < 1:
            is_valid = False
            flash("First Name required.", "regError")
        elif len(user["first_name"]) < 2:
            is_valid = False
            flash("First Name Must Be Longer", "regError")
        if len(user["last_name"]) < 1:
            is_valid = False
            flash("Last Name required.", "regError")
        elif len(user["last_name"]) < 2:
            is_valid = False
            flash("Last Name Must Be Longer", "regError")
        if len(user["email"]) < 1:
            is_valid = False
            flash("Email Required.", "regError")
        elif not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email", "regError")
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(mydb).query_db(query)
        output = []
        for user_dictionary in results:
            output.append( cls(user_dictionary) )
        return output

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email) VALUES(%(first_name)s,%(last_name)s,%(email)s);"
        result = connectToMySQL(mydb).query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(mydb).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)