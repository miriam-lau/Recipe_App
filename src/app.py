from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from entities.cookbook import Cookbook
from entities.cookbook_manager import CookbookManager
from entities.recipe import Recipe
from entities.recipe_manager import RecipeManager
from entities.entry import Entry
from entities.entry_manager import EntryManager

app = Flask(__name__)
cookbook_manager: CookbookManager = None
recipe_manager: RecipeManager = None
entry_manager: EntryManager = None


def initialize_app():
    global cookbook_manager
    global recipe_manager
    global entry_manager
    cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager()
    recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager)
    entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager)


@app.route("/")
def render_cookbooks():
    cookbooks = cookbook_manager.get_cookbooks()
    return render_template(
        'cookbooks.html',**locals())


@app.route("/addcookbook", methods=["POST"])
def add_cookbook():
    cookbook = Cookbook(None, request.form["cookbook_name"], request.form["cookbook_notes"])
    cookbook_manager.add_new_cookbook(cookbook)
    return redirect(url_for("render_cookbooks"))


@app.route("/cookbook/<int:id>")
def render_cookbook(id: int):
    cookbook = cookbook_manager.get_cookbook(id)
    return render_template(
        'cookbook.html',**locals())


@app.route("/addrecipe", methods=["POST"])
def add_recipe():
    cookbook_id = int(request.form["recipe_cookbook_id"])
    priority_input = request.form["recipe_priority"]
    recipe = Recipe(None, cookbook_id, request.form["recipe_name"], int(priority_input) if priority_input else 0,
                    False, request.form["recipe_category"], request.form["recipe_notes"])
    recipe_manager.add_new_recipe(cookbook_manager, recipe)
    return redirect(url_for("render_cookbook", id=cookbook_id))


@app.route("/recipe/<int:id>")
def render_recipe(id: int):
    recipe = recipe_manager.get_recipe(id)
    cookbook = cookbook_manager.get_cookbook(recipe.cookbook_id)
    return render_template(
        'recipe.html',**locals())


@app.route("/addentry", methods=["POST"])
def add_entry():
    recipe_id = int(request.form["entry_recipe_id"])
    entry = Entry(None, recipe_id, request.form["entry_date"], \
                  float(request.form["entry_miriam_rating"]), float(request.form["entry_james_rating"]), \
                  request.form["entry_miriam_comments"], request.form["entry_james_comments"])
    entry_manager.add_new_entry(recipe_manager, entry)
    return redirect(url_for("render_recipe", id=recipe_id))


initialize_app()
