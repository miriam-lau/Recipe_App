from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from .entities.cookbook import Cookbook
from .entities.cookbook_manager import CookbookManager
from .entities.recipe import Recipe
from .entities.recipe_manager import RecipeManager
from .entities.entry import Entry
from .entities.entry_manager import EntryManager
from .settings import settings
import datetime


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
    debug_mode = settings.get_debug_mode()
    cookbooks = cookbook_manager.get_cookbooks()
    return render_template(
        'cookbooks.html',**locals())


@app.route("/addcookbook", methods=["POST"])
def add_cookbook():
    cookbook = Cookbook(None, request.form["cookbook_name"], request.form["cookbook_notes"])
    cookbook_manager.add_new_cookbook(cookbook)
    return redirect(url_for("render_cookbooks"))


@app.route("/cookbook/edit/<int:id>", methods=["POST"])
def edit_cookbook(id: int):
    cookbook_manager.modify_cookbook(id, request.form["cookbook_name"], request.form["cookbook_notes"])
    return redirect(url_for("render_cookbook", id=id))


@app.route("/deletecookbook/<int:id>", methods=["POST"])
def delete_cookbook(id: int):
    if request.form["cookbook_delete"] != "delete":
        return redirect(url_for("edit_cookbook", id=id))

    cookbook_manager.delete_cookbook(recipe_manager, entry_manager, id)
    return redirect(url_for("render_cookbooks"))


@app.route("/cookbook/view/<int:id>")
def render_cookbook(id: int):
    debug_mode = settings.get_debug_mode()
    cookbook = cookbook_manager.get_cookbook(id)
    return render_template('cookbook.html',**locals())


@app.route("/cookbook/edit/<int:id>")
def render_edit_cookbook(id: int):
    debug_mode = settings.get_debug_mode()
    cookbook = cookbook_manager.get_cookbook(id)
    return render_template('edit_cookbook.html',**locals())


@app.route("/addrecipe", methods=["POST"])
def add_recipe():
    cookbook_id = int(request.form["recipe_cookbook_id"])
    priority_input = request.form["recipe_priority"]
    recipe = Recipe(None, cookbook_id, request.form["recipe_name"], int(priority_input) if priority_input else 0,
                    False, request.form["recipe_category"], request.form["recipe_notes"])
    recipe_manager.add_new_recipe(cookbook_manager, recipe)
    return redirect(url_for("render_cookbook", id=cookbook_id))


@app.route("/recipe/edit/<int:id>", methods=["POST"])
def edit_recipe(id: int):
    recipe_manager.modify_recipe(
        id, request.form["recipe_name"], request.form["recipe_category"], int(request.form["recipe_priority"]), \
        request.form["recipe_has_image"].lower() == 'true', request.form["recipe_notes"])
    return redirect(url_for("render_recipe", id=id))


@app.route("/deleterecipe/<int:id>", methods=["POST"])
def delete_recipe(id: int):
    if request.form["recipe_delete"] != "delete":
        return redirect(url_for("edit_recipe", id=id))

    cookbook_id = recipe_manager.get_recipe(id).cookbook_id
    recipe_manager.delete_recipe(cookbook_manager, entry_manager, id)
    return redirect(url_for("render_cookbook", id=cookbook_id))


@app.route("/recipe/view/<int:id>")
def render_recipe(id: int):
    debug_mode = settings.get_debug_mode()
    recipe = recipe_manager.get_recipe(id)
    cookbook = cookbook_manager.get_cookbook(recipe.cookbook_id)
    return render_template('recipe.html',**locals())


@app.route("/recipe/edit/<int:id>")
def render_edit_recipe(id: int):
    debug_mode = settings.get_debug_mode()
    recipe = recipe_manager.get_recipe(id)
    cookbook = cookbook_manager.get_cookbook(recipe.cookbook_id)
    return render_template('edit_recipe.html',**locals())


@app.route("/addentry", methods=["POST"])
def add_entry():
    recipe_id = int(request.form["entry_recipe_id"])
    entry = Entry(None, recipe_id, datetime.datetime.strptime(request.form["entry_date"], '%Y-%m-%d'), \
                  float(request.form["entry_miriam_rating"]), float(request.form["entry_james_rating"]), \
                  request.form["entry_miriam_comments"], request.form["entry_james_comments"])
    entry_manager.add_new_entry(recipe_manager, entry)
    return redirect(url_for("render_recipe", id=recipe_id))


@app.route("/entry/edit/<int:id>", methods=["POST"])
def edit_entry(id: int):
    entry_manager.modify_entry(
        id, datetime.datetime.strptime(request.form["entry_date"], '%Y-%m-%d'), \
        float(request.form["entry_miriam_rating"]), float(request.form["entry_james_rating"]), \
        request.form["entry_miriam_comments"], request.form["entry_james_comments"])
    return redirect(url_for("render_entry", id=id))


@app.route("/deleteentry/<int:id>", methods=["POST"])
def delete_entry(id: int):
    if request.form["entry_delete"] != "delete":
        return redirect(url_for("edit_entry", id=id))

    recipe_id = entry_manager.get_entry(id).recipe_id
    entry_manager.delete_entry(recipe_manager, id)
    return redirect(url_for("render_recipe", id=recipe_id))


@app.route("/entry/view/<int:id>")
def render_entry(id: int):
    debug_mode = settings.get_debug_mode()
    entry = entry_manager.get_entry(id)
    recipe = recipe_manager.get_recipe(entry.recipe_id)
    return render_template('entry.html',**locals())


@app.route("/entry/edit/<int:id>")
def render_edit_entry(id: int):
    debug_mode = settings.get_debug_mode()
    entry = entry_manager.get_entry(id)
    recipe = recipe_manager.get_recipe(entry.recipe_id)
    return render_template('edit_entry.html',**locals())


initialize_app()
