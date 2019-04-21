from sqlalchemy.sql import func, expression
from flask import flash
from config import db, bcrypt
import re
from datetime import datetime, date



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=\S{5,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')



class Users(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(145))
    last_name = db.Column(db.String(145))
    email = db.Column(db.String(125))
    dojo_location = db.Column(db.String(125))
    password = db.Column(db.String(125))
    birth_date = db.Column(db.DateTime)

    recipes_of_user = db.relationship('Recipes', backref='author', lazy='dynamic')
    likes_of_user = db.relationship('Likes', backref='author', lazy='dynamic')


    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if len(user_data["first_name"]) < 1:
            is_valid = False
            flash("Please provide a first name")
        if len(user_data["last_name"]) < 1:
            is_valid = False
            flash("Please provide a last name")
        if not EMAIL_REGEX.match(user_data["email"]):
            is_valid = False
            flash("Please provide a valid email")
        if len(user_data["password"]) < 8:
            is_valid = False
            flash("Password should be at least 8 characters")
        if user_data["password"] != user_data["cpassword"]:
            is_valid = False
            flash("Passwords do not match")
        return is_valid

    @classmethod
    def validate_login(cls, user_data):
        is_valid = True
        result = Users.query.filter_by(email = user_data["username"]).first()

        if not EMAIL_REGEX.match(user_data["username"]):
            is_valid = False
            flash("Please provide a valid email")
        if len(user_data["password"]) < 3:
            is_valid = False
            flash("Password should be at least 8 characters")
        if result:
            if not bcrypt.check_password_hash(result.password, user_data['password']):
                is_valid = False
                flash("Passwords incorrect")
        return is_valid

    @classmethod
    def add_new_user(cls, user_data):
        hashed_password = bcrypt.generate_password_hash(user_data["password"])
        user_to_add = cls(first_name=user_data["first_name"], last_name=user_data["last_name"], email=user_data["email"], password=hashed_password)
        db.session.add(user_to_add)
        db.session.commit()
        return user_to_add
    
    @classmethod
    def validate_age(cls, user_data):
        valid_age =True
        input = user_data["birth_date"]
        birthday = datetime.strptime(input, "%Y-%m-%d")
        today = date.today()
        if (today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))) <18:
            valid_age =False
            flash("Invalid Age")

        return valid_age




class Recipes(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    rname = db.Column(db.String(145))
    description = db.Column(db.String(245))
    instructions = db.Column(db.String(345))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # author = db.relationship('Users', foreign_keys=[user_id], backref="author", cascade="all") #from one to many relationship, other tutorials do not recommend

    likes_of_recipe = db.relationship('Likes', backref='recipe_like', lazy='dynamic')

    under_30 = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_recipe(cls, user_data):
        is_valid = True
        if len(user_data["rname"]) < 3:
            is_valid = False
            flash("Please provide valid recipe name, at least 3 char")
        if len(user_data["description"]) < 10:
            is_valid = False
            flash("Please provide valid recipe desc, at least 10 char")
        return is_valid

    @classmethod
    def add_new_recipe(cls, user_data):
        u30=True
        if user_data["under_30"] == "No":
            u30=False
        print(user_data["under_30"])
        recipe_to_add = cls(rname=user_data["rname"], description=user_data["description"], instructions=user_data["instructions"], under_30=u30)
        print(recipe_to_add)
        db.session.add(recipe_to_add)
        db.session.commit()
        return recipe_to_add

class Likes(db.Model):	
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # author = db.relationship('Users', foreign_keys=[user_id], backref="recipes_of_user", cascade="all") #from one to many relationship, other tutorials do not recommend
  
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    # recipe_like = db.relationship('Recipes', foreign_keys=[recipe_id], backref="likes_of_recipe", cascade="all") #from one to many relationship, other tutorials do not recommend

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())