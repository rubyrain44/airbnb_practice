from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user

class Home:
    def __init__(self, data):
        self.id = data['id']
        self.street = data['id']
        self.city = data['city']
        self.state = data['state']
        self.bedrooms = data['bedrooms']
        self.bathrooms = data['bathrooms']
        self.amenities = data['amenities']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None



# GET ALL METHODS --------------------------------------
    @classmethod
    def get_all_homes(cls):
        query = """
                SELECT * FROM homes;
                """
        results = connectToMySQL('vacation_app').query_db(query)
        homes = []
        for home in results:
            homes.append(cls(home))
        return homes

    @classmethod
    def get_all_hosted_homes_with_user(cls):
        query = """
                SELECT * FROM homes
                LEFT JOIN users
                ON users.id = homes.user_id;
                """
        results = connectToMySQL('vacation_app').query_db(query)
        all_homes_with_creator = []
        for row in results:
            one_home = cls(row)
            home_creator = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'username' : row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_home.creator = user.User(home_creator)
            all_homes_with_creator.append(one_home)
        return all_homes_with_creator


# GET SINGLE METHODS --------------------------------------
    @classmethod
    def get_home(cls, data):
        query = """
                SELECT * FROM homes
                WHERE id = %(id)s;
                """
        results = connectToMySQL('vacation_app').query_db(query, data)
        return cls(results[0])
        
    @classmethod
    def get_hosted_home_with_user(cls, data):
        query = """
                SELECT * FROM homes
                LEFT JOIN users
                ON homes.user_id = users.id
                WHERE homes.id = %(id)s;
                """
        results = connectToMySQL('vacation_app').query_db(query, data)
        home = cls(results[0])
        home_creator = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'username' : results[0]['username'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
            }
        home.creator = user.User(home_creator)
        return home


# OTHER METHODS -------------------------------------------

        self.id = data['id']
        self.street = data['id']
        self.city = data['city']
        self.state = data['state']
        self.bedrooms = data['bedrooms']
        self.bathrooms = data['bathrooms']
        self.amenities = data['amenities']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def add_home(cls, data):
        query = """
                INSERT INTO homes
                (street, city, state, bedrooms, bathrooms, amenities, description, user_id) VALUES
                (%(street)s, %(city)s, %(state)s, %(bedrooms)s, %(bathrooms)s, %(amenities)s, %(description)s, %(user_id)s);
                """
        return connectToMySQL('vacation_app').query_db(query, data)

    @classmethod
    def edit_home(cls, data):
        query = """
                UPDATE homes SET
                street=%(street)s, city=%(city)s, state=%(state)s, bedrooms=%(bedrooms)s, bathrooms=%(bathrooms)s, amenities=%(amenities)s, description=%(description)s, updated_at = NOW ()
                WHERE id = %(id)s;
                """
        return connectToMySQL('vacation_app').query_db(query, data)

    @classmethod
    def delete_home(cls, data):
        query = """
                DELETE FROM homes
                WHERE id = %(id)s;
                """
        return connectToMySQL('vacation_app').query_db(query, data)

# ====================================================================

# VALIDATIONS FOR MAGAZINE CREATION
    @staticmethod
    def validate_home(form_data):
        is_valid = True
        if len(form_data['street']) < 2:
            flash("Street must be at least 2 characters.")
            is_valid = False

        if len(form_data['state']) < 2:
            flash("State must be at least 2 characters.")
            is_valid = False

        if len(form_data['state']) > 2:
            flash("City must be 2 characters.")
            is_valid = False

        if len(form_data['description']) < 10:
            flash("Description must be at least 10 characters long.")
            is_valid = False
        return is_valid