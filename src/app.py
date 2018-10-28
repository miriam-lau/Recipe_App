from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from .entities.cookbook_manager import CookbookManager
from .entities.recipe_manager import RecipeManager
from .entities.entry_manager import EntryManager
from .settings.settings import Settings
import datetime


app = Flask(__name__)
cookbook_manager: CookbookManager = None
recipe_manager: RecipeManager = None
entry_manager: EntryManager = None
settings: Settings = None


def initialize_app():
    global cookbook_manager
    global recipe_manager
    global entry_manager
    global settings
    settings = Settings()
    cookbook_manager = CookbookManager(settings)
    recipe_manager = RecipeManager(settings)
    entry_manager = EntryManager(settings)
    cookbook_manager.children_entity_manager = recipe_manager
    recipe_manager.parent_entity_manager = cookbook_manager
    recipe_manager.children_entity_manager = entry_manager
    entry_manager.parent_entity_manager = recipe_manager
    cookbook_manager.initialize()
    recipe_manager.initialize()
    entry_manager.initialize()


@app.route("/")
def render_cookbooks():
    debug_mode = settings.debug_mode
    cookbooks = cookbook_manager.get_cookbooks()
    return render_template(
        'cookbooks.html',**locals())


@app.route("/addcookbook", methods=["POST"])
def add_cookbook():
    cookbook_manager.add_new_entity(None, (request.form["cookbook_name"], request.form["cookbook_notes"]))
    return redirect(url_for("render_cookbooks"))


@app.route("/editcookbook/<int:entity_id>", methods=["POST"])
def edit_cookbook(entity_id: int):
    cookbook_manager.modify_entity(entity_id, {'name': request.form["cookbook_name"], 'notes': request.form["cookbook_notes"]})
    return redirect(url_for("render_cookbook", entity_id=entity_id))


@app.route("/deletecookbook/<int:entity_id>", methods=["POST"])
def delete_cookbook(entity_id: int):
    if request.form["cookbook_delete"] != "delete":
        return redirect(url_for("render_edit_cookbook", entity_id=entity_id))

    cookbook_manager.delete_entity(entity_id)
    return redirect(url_for("render_cookbooks"))


@app.route("/cookbook/view/<int:entity_id>")
def render_cookbook(entity_id: int):
    debug_mode = settings.debug_mode
    cookbook = cookbook_manager.get_cookbook(entity_id)
    return render_template('cookbook.html',**locals())


@app.route("/cookbook/edit/<int:entity_id>")
def render_edit_cookbook(entity_id: int):
    debug_mode = settings.debug_mode
    cookbook = cookbook_manager.get_cookbook(entity_id)
    return render_template('edit_cookbook.html',**locals())


@app.route("/addrecipe", methods=["POST"])
def add_recipe():
    recipe = recipe_manager.add_new_entity(
        int(request.form["recipe_cookbook_id"]), (request.form["recipe_name"], \
        request.form["recipe_priority"], "False", request.form["recipe_category"], request.form["recipe_notes"]))
    return redirect(url_for("render_cookbook", entity_id=recipe.cookbook_id))


@app.route("/recipe/uploadimage/<int:entity_id>", methods=["POST", "GET"])
def upload_recipe_image(entity_id: int):
    recipe_manager.upload_recipe_image(entity_id, request.files['file'])
    return redirect(url_for("render_recipe", entity_id=entity_id))


@app.route("/editrecipe/<int:entity_id>", methods=["POST"])
def edit_recipe(entity_id: int):
    recipe_has_image = False
    if "recipe_has_image" in request.form:
        recipe_has_image = request.form["recipe_has_image"].lower() == "true"
    recipe_manager.modify_recipe(
        entity_id, (request.form["recipe_name"], request.form["recipe_priority"], \
        "True" if recipe_has_image else "False", request.form["recipe_category"], request.form["recipe_notes"]))
    return redirect(url_for("render_recipe", entity_id=entity_id))


@app.route("/deleterecipe/<int:entity_id>", methods=["POST"])
def delete_recipe(entity_id: int):
    if request.form["recipe_delete"] != "delete":
        return redirect(url_for("render_edit_recipe", entity_id=entity_id))

    cookbook_id = recipe_manager.get_recipe(entity_id).cookbook_id
    recipe_manager.delete_entity(entity_id)
    return redirect(url_for("render_cookbook", entity_id=cookbook_id))


@app.route("/recipe/view/<int:entity_id>")
def render_recipe(entity_id: int):
    debug_mode = settings.debug_mode
    recipe = recipe_manager.get_recipe(entity_id)
    cookbook = cookbook_manager.get_cookbook(recipe.cookbook_id)
    return render_template('recipe.html',**locals())


@app.route("/recipe/edit/<int:entity_id>")
def render_edit_recipe(entity_id: int):
    debug_mode = settings.debug_mode
    recipe = recipe_manager.get_recipe(entity_id)
    cookbook = cookbook_manager.get_cookbook(recipe.cookbook_id)
    return render_template('edit_recipe.html',**locals())


@app.route("/addentry", methods=["POST"])
def add_entry():
    entry = entry_manager.add_new_entity(
        int(request.form["entry_recipe_id"]), (request.form["entry_date"], \
        request.form["entry_miriam_rating"], request.form["entry_james_rating"], \
        request.form["entry_miriam_comments"], request.form["entry_james_comments"]))
    return redirect(url_for("render_recipe", entity_id=entry.recipe_id))


@app.route("/editentry/<int:entity_id>", methods=["POST"])
def edit_entry(entity_id: int):
    entry_manager.modify_entity(
        entity_id, (request.form["entry_date"], \
        request.form["entry_miriam_rating"], request.form["entry_james_rating"], \
        request.form["entry_miriam_comments"], request.form["entry_james_comments"]))
    return redirect(url_for("render_entry", entity_id=entity_id))


@app.route("/deleteentry/<int:entity_id>", methods=["POST"])
def delete_entry(entity_id: int):
    if request.form["entry_delete"] != "delete":
        return redirect(url_for("render_edit_entry", entity_id=entity_id))

    recipe_id = entry_manager.get_entry(entity_id).recipe_id
    entry_manager.delete_entity(entity_id)
    return redirect(url_for("render_recipe", entity_id=recipe_id))


@app.route("/entry/view/<int:entity_id>")
def render_entry(entity_id: int):
    debug_mode = settings.debug_mode
    entry = entry_manager.get_entry(entity_id)
    recipe = recipe_manager.get_recipe(entry.recipe_id)
    return render_template('entry.html',**locals())


@app.route("/entry/edit/<int:entity_id>")
def render_edit_entry(entity_id: int):
    debug_mode = settings.debug_mode
    entry = entry_manager.get_entry(entity_id)
    recipe = recipe_manager.get_recipe(entry.recipe_id)
    return render_template('edit_entry.html',**locals())


@app.route('/serveimage/<path:filename>')
def serve_image(filename):
    return send_from_directory(settings.recipe_app_directory + "RecipeImages/",
                               filename, as_attachment=True)


initialize_app()
