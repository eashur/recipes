from config import app
from controller_functions import index, add_newuser, delete_receipe, viewall, login, create, logout, like, dashboard,review, view_instruction, add_recipe


app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=add_newuser, methods=["POST"])
app.add_url_rule("/review", view_func=review, methods=["Get", "POST"])
app.add_url_rule("/dashboard", view_func=dashboard)
app.add_url_rule("/create", view_func=create, methods=["Get", "POST"])
app.add_url_rule("/delete", view_func=delete_receipe, methods=["Get", "POST"])
app.add_url_rule("/add_recipe", view_func=add_recipe, methods=["Get", "POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/like", view_func=like, methods=["POST"])
app.add_url_rule("/view_all", view_func=viewall, methods=["POST"])
app.add_url_rule("/", view_func=logout)

app.add_url_rule("/instructions/<recipe_id>", view_func=view_instruction, methods=["POST"])

