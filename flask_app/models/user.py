from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app.models import home

### MODEL ###

class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.hosted_homes = []


### CLASS METHODS ###

    #Register/Create A User
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, username, email, password) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);"
        return connectToMySQL('vacation_app').query_db(query, data)


    #Find A User By ID
    @classmethod
    def get_user(cls, data):
        print('a')
        query = "SELECT * FROM users WHERE id = %(id)s;"
        print('b')
        results = connectToMySQL('vacation_app').query_db(query, data)
        print(results)
        return cls(results[0])


    #Find A User By Email (with the ability to see if the email exists or not already)
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('vacation_app').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

### VALIDATIONS ###

    #Validations On User Creation
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['username']) < 2:
            flash("Username must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['register_password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if (data['register_password']) != (data['confirm_password']):
            flash("Passwords must match!")
            is_valid = False
        return is_valid