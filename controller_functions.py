from flask import Flask, render_template, redirect, request, session, flash
from config import app, db
from models import Users, Recipes, Likes

def index():
    session.clear()
    return render_template("index.html" )

def dashboard():
    
    # list_of_all_dojos = Users.query.all()

    return render_template("dashboard.html", name = session["first_name"])

def review():
    try:
        fname = session["first_name"]
        list_of_all_recipes = Recipes.query.all()
        return render_template("review.html", name = fname, recipes=list_of_all_recipes )
    except:
        flash("Please login!")
        return redirect("/")

def viewall():
    try:
        fname = session["first_name"]
        list_of_all_recipes = Recipes.query.all()
        return render_template("review.html", name = fname, recipes=list_of_all_recipes )
    except:
        flash("Please login!")
        list_of_all_recipes = Recipes.query.all()
        return render_template("viewAll.html", recipes=list_of_all_recipes )


def create():
    
    # list_of_all_dojos = Users.query.all()

    return render_template("create.html", user_id = session["user_id"])

def add_newuser():
    validation_check = Users.validate_user(request.form)
    if not validation_check:        
       return redirect("/")
    else:
        flash("Successfully registered")
        new_user = Users.add_new_user(request.form)
        session["user_id"] = new_user.id
        session["first_name"] = new_user.first_name
        print(session["first_name"])
        return redirect("/dashboard")

def add_recipe():
    validation_check = Recipes.validate_recipe(request.form)
    if not validation_check:
        print("cannot validate reciepr <><><><><<><<><><>>><><><><<><><")    
        return redirect("/create")
    else:
        flash("Successfully created")
        print("Cooool Adding recept  <><><><><<><<><><>>><><><><<><><")  
        new_recipe = Recipes.add_new_recipe(request.form)
        return redirect("/review")

def view_instruction(recipe_id):
    recipe_id = request.form["recipe_id"]
    the_recipe = Recipes.query.filter_by(id=recipe_id).first()
    return render_template("intruction.html", recipe=the_recipe)

def delete_receipe():
    recipe_id = request.form["recipe_id"]
    the_recipe = Recipes.query.filter_by(id=recipe_id).first()
    db.session.delete(the_recipe)
    db.session.commit()
    return redirect("/review")
    
    

def login():
    validation_check = Users.validate_login(request.form)
    if not validation_check:        
       return redirect("/")
    else:
        # list_of_all_users = Users.query.all()
        result = Users.query.filter_by(email = request.form["username"]).first()
        session["first_name"] = result.first_name
        session["user_id"] = result.id
        return redirect("/dashboard")

        # return render_template("users.html", users = list_of_all_users, name = result.first_name )

def logout():
    session.clear()

    return redirect("/")

def like():
    flash("This function is still in development!!!!")

    return redirect("/login")