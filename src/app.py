from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from .entities.cookbook_manager import CookbookManager
from .entities.recipe_manager import RecipeManager
from .entities.entry_manager import EntryManager
from .entities.city_manager import CityManager
from .entities.restaurant_manager import RestaurantManager
from .entities.dish_manager import DishManager
from .entities.dish_entry_manager import DishEntryManager
from .settings.settings import Settings
from .entities.cookbook import Cookbook
from .entities.recipe import Recipe
from .entities.entry import Entry
from .entities.city import City
from .entities.restaurant import Restaurant
from .entities.dish import Dish
from .entities.dish_entry import DishEntry
import datetime


app = Flask(__name__)
cookbook_manager: CookbookManager = None
recipe_manager: RecipeManager = None
entry_manager: EntryManager = None
city_manager: CityManager = None
restaurant_manager: RestaurantManager = None
dish_manager: DishManager = None
dish_entry_manager: DishEntryManager = None
settings: Settings = None


def initialize_app():
    global cookbook_manager
    global recipe_manager
    global entry_manager

    global city_manager
    global restaurant_manager
    global dish_manager
    global dish_entry_manager

    global settings
    settings = Settings()

    cookbook_manager = CookbookManager(settings)
    recipe_manager = RecipeManager(settings)
    entry_manager = EntryManager(settings)
    cookbook_manager.children_entity_manager = recipe_manager
    recipe_manager.parent_entity_manager = cookbook_manager
    recipe_manager.children_entity_manager = entry_manager
    entry_manager.parent_entity_manager = recipe_manager

    city_manager = CityManager(settings)
    restaurant_manager = RestaurantManager(settings)
    dish_manager = DishManager(settings)
    dish_entry_manager = DishEntryManager(settings)
    city_manager.children_entity_manager = restaurant_manager
    restaurant_manager.parent_entity_manager = city_manager
    restaurant_manager.children_entity_manager = dish_manager
    dish_manager.parent_entity_manager = restaurant_manager
    dish_manager.children_entity_manager = dish_entry_manager
    dish_entry_manager.parent_entity_manager = dish_manager

    cookbook_manager.initialize()
    recipe_manager.initialize()
    entry_manager.initialize()

    city_manager.initialize()
    restaurant_manager.initialize()
    dish_manager.initialize()
    dish_entry_manager.initialize()


@app.route("/")
def render_main():
    debug_mode = settings.debug_mode
    return render_template('main.html', **locals())


@app.route("/cities")
def render_cities():
    debug_mode = settings.debug_mode
    cities = city_manager.get_sorted_cities()

    has_info_template = False
    has_children_list_template = True
    has_add_child_template = True

    # Title section
    title = "Cities"

    # Children list section
    child_table_headers = [
        "Name", "State", "Country", "Notes"]
    child_table_values = []

    for city in cities:
        child_table_values.append({
            "link": "/city/view/%s" % city.entity_id,
            "row": [city.name, city.state, city.country, city.notes]})

    # Add child section
    add_child_link = "/addcity"
    add_child_title = "Add City"

    add_child_dicts = [
        create_add_child_dict("Name", "city_name", "", "Name"),
        create_add_child_dict("State", "city_state", "", "State"),
        create_add_child_dict("Country", "city_country", "", "Country"),
        create_add_child_dict("Notes", "city_notes", "", "Notes")
    ]

    return render_template('view_entity.html', **locals())


@app.route("/cookbooks")
def render_cookbooks():
    debug_mode = settings.debug_mode
    cookbooks = cookbook_manager.get_sorted_cookbooks()

    has_info_template = False
    has_children_list_template = True
    has_add_child_template = True

    back_link = "/"
    back_text = "Back to main page"

    # Title section
    title = "Cookbooks"

    # Children list section
    child_table_headers = [
        "Name", "Num recipes made", "Success rate", "Num recipes we want to make"]
    child_table_values = []

    for cookbook in cookbooks:
        child_table_values.append({
            "link": "/cookbook/view/%s" % cookbook.entity_id,
            "row": [cookbook.name, str(cookbook.num_recipes_made()), "%s%%" % cookbook.success_percentage(),
             str(cookbook.num_recipes_want_to_make())]})

    # Add child section
    add_child_link = "/addcookbook"
    add_child_title = "Add Cookbook"

    add_child_dicts = [
        create_add_child_dict("Name", "cookbook_name", "", "Cookbook name"),
        create_add_child_dict("Notes", "cookbook_notes", "", "Cookbook notes")
    ]

    return render_template('view_entity.html', **locals())


@app.route("/addcookbook", methods=["POST"])
def add_cookbook():
    cookbook_manager.add_new_entity(None, {
        Cookbook.NAME_HEADER: request.form["cookbook_name"],
        Cookbook.NOTES_HEADER: request.form["cookbook_notes"]})
    return redirect(url_for("render_cookbooks"))


@app.route("/editcookbook/<int:entity_id>", methods=["POST"])
def edit_cookbook(entity_id: int):
    cookbook_manager.modify_entity(entity_id,
                                   {Cookbook.NAME_HEADER: request.form["cookbook_name"],
                                    Cookbook.NOTES_HEADER: request.form["cookbook_notes"]})
    return redirect(url_for("render_cookbook", entity_id=entity_id))


@app.route("/deletecookbook/<int:entity_id>", methods=["POST"])
def delete_cookbook(entity_id: int):
    if request.form["cookbook_delete"] != "delete":
        return redirect(url_for("render_edit_cookbook", entity_id=entity_id))

    cookbook_manager.delete_entity(entity_id)
    return redirect(url_for("render_cookbooks"))


@app.route("/cookbook/view/<int:entity_id>")
def render_cookbook(entity_id: int):
    has_info_template = True
    has_children_list_template = True
    has_add_child_template = True

    debug_mode = settings.debug_mode
    cookbook = cookbook_manager.get_entity(entity_id)

    # Title section
    back_link = "/cookbooks"
    back_text = "Back to cookbooks page"
    edit_link = "/cookbook/edit/%s" % cookbook.entity_id
    title = cookbook.name

    # Info section
    info_dicts = [
        create_info_dict("Num recipes made", str(cookbook.num_recipes_made())),
        create_info_dict("Success rate", "%s%%" % cookbook.success_percentage()),
        create_info_dict("Num recipes we want to make", str(cookbook.num_recipes_want_to_make())),
        create_info_dict("Notes", cookbook.notes)
    ]

    # Children list section
    child_table_headers = [
        "Name", "Num times made", "Best rating", "Latest rating", "Priority", "Category"]
    child_table_values = []

    for recipe in cookbook.recipes_by_best_rating_descending():
        child_table_values.append({
            "link": "/recipe/view/%s" % recipe.entity_id,
            "row": [recipe.name,
                    str(recipe.get_num_times_made()),
                    str(recipe.get_best_rating()),
                    str(recipe.get_latest_rating()),
                    str(recipe.priority),
                    recipe.category]})

    # Add child section
    add_child_link = "/addrecipe"
    add_child_title = "Add Recipe"

    add_child_dicts = [
        create_add_child_dict("Name", "recipe_name", "", "Name"),
        create_add_child_dict("Category", "recipe_category", "", "Category"),
        create_add_child_dict("Priority", "recipe_priority", "", "Priority"),
        create_add_child_dict("Notes", "recipe_notes", "", "Notes")]

    add_child_hidden_dicts = [
        create_add_child_hidden_dict("recipe_cookbook_id", str(cookbook.entity_id))
    ]

    return render_template('view_entity.html', **locals())


@app.route("/cookbook/edit/<int:entity_id>")
def render_edit_cookbook(entity_id: int):
    debug_mode = settings.debug_mode
    cookbook = cookbook_manager.get_entity(entity_id)

    # Title section
    back_link = "/"
    back_text = "Back to main page"
    view_link = "/cookbook/view/%s" % cookbook.entity_id
    title = cookbook.name

    # Info section
    edit_entity_link = "/editcookbook/%s" % cookbook.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", "cookbook_name", cookbook.name),
        create_edit_info_dict("Notes", "cookbook_notes", cookbook.notes)
    ]

    delete_link = "/deletecookbook/%s" % cookbook.entity_id
    delete_id = "cookbook_delete"

    return render_template('edit_entity.html', **locals())


@app.route("/addrecipe", methods=["POST"])
def add_recipe():
    recipe = recipe_manager.add_new_entity(
        int(request.form["recipe_cookbook_id"]), {
            Recipe.NAME_HEADER: request.form["recipe_name"],
            Recipe.PRIORITY_HEADER: request.form["recipe_priority"],
            Recipe.HAS_IMAGE_HEADER: "False",
            Recipe.CATEGORY_HEADER: request.form["recipe_category"],
            Recipe.NOTES_HEADER: request.form["recipe_notes"]})
    return redirect(url_for("render_cookbook", entity_id=recipe.parent_id))


@app.route("/recipe/uploadimage/<int:entity_id>", methods=["POST", "GET"])
def upload_recipe_image(entity_id: int):
    recipe_manager.upload_recipe_image(entity_id, request.files['file'])
    return redirect(url_for("render_recipe", entity_id=entity_id))


@app.route("/editrecipe/<int:entity_id>", methods=["POST"])
def edit_recipe(entity_id: int):
    recipe_manager.modify_entity(
        entity_id, {
            Recipe.NAME_HEADER: request.form["recipe_name"],
            Recipe.PRIORITY_HEADER: request.form["recipe_priority"],
            Recipe.HAS_IMAGE_HEADER: request.form["recipe_has_image"],
            Recipe.CATEGORY_HEADER: request.form["recipe_category"],
            Recipe.NOTES_HEADER: request.form["recipe_notes"]})
    return redirect(url_for("render_recipe", entity_id=entity_id))


@app.route("/deleterecipe/<int:entity_id>", methods=["POST"])
def delete_recipe(entity_id: int):
    if request.form["recipe_delete"] != "delete":
        return redirect(url_for("render_edit_recipe", entity_id=entity_id))

    cookbook_id = recipe_manager.get_entity(entity_id).parent_id
    recipe_manager.delete_entity(entity_id)
    return redirect(url_for("render_cookbook", entity_id=cookbook_id))


@app.route("/recipe/view/<int:entity_id>")
def render_recipe(entity_id: int):
    has_info_template = True
    has_children_list_template = True
    has_add_child_template = True

    debug_mode = settings.debug_mode
    recipe = recipe_manager.get_entity(entity_id)
    cookbook = recipe.parent

    # Title section
    back_link = "/cookbook/view/%s" % cookbook.entity_id
    back_text = "Back to %s page" % cookbook.name
    edit_link = "/recipe/edit/%s" % recipe.entity_id
    title = "%s: %s" % (cookbook.name, recipe.name)

    # Info section
    info_image_name = None
    if recipe.has_image:
        info_image_name = "/serveimage/%s.jpg" % recipe.entity_id

    info_dicts = [
        create_info_dict("Best rating", str(recipe.get_best_rating())),
        create_info_dict("Latest rating", str(recipe.get_latest_rating())),
        create_info_dict("Num times made", str(recipe.get_num_times_made())),
        create_info_dict("Category", str(recipe.category)),
        create_info_dict("Priority", str(recipe.priority)),
        create_info_dict("Notes", recipe.notes)
    ]

    # Children list section
    child_table_headers = [
        "Date", "Overall Rating", "Miriam's Rating", "Miriam's Comments", "James' Rating", "James' Comments"]
    child_table_values = []

    for entry in recipe.entries_by_date_descending():
        child_table_values.append({
            "link": "/entry/view/%s" % entry.entity_id,
            "row": [entry.date_string(), entry.get_overall_rating(), entry.miriam_rating, entry.miriam_comments,
             entry.james_rating, entry.james_comments]})

    # Add child section
    add_child_link = "/addentry"
    add_child_title = "Add Entry"

    add_child_dicts = [
        create_add_child_dict("Date", "entry_date", datetime.datetime.today().strftime('%Y-%m-%d'), ""),
        create_add_child_dict("Miriam's Rating", "entry_miriam_rating", "", "Miriam's rating"),
        create_add_child_dict("Miriam's Comments", "entry_miriam_comments", "", "Miriam's comments"),
        create_add_child_dict("James' Rating", "entry_james_rating", "", "James' rating"),
        create_add_child_dict("James' Comments", "entry_james_comments", "", "James' comments"),
    ]

    add_child_hidden_dicts = [
        create_add_child_hidden_dict("entry_recipe_id", str(recipe.entity_id))
    ]

    return render_template('view_entity.html', **locals())


@app.route("/recipe/edit/<int:entity_id>")
def render_edit_recipe(entity_id: int):
    debug_mode = settings.debug_mode
    recipe = recipe_manager.get_entity(entity_id)
    cookbook = recipe.parent

    # Title section
    back_link = "/cookbook/view/%s" % cookbook.entity_id
    back_text = "Back to %s page" % cookbook.name
    view_link = "/recipe/view/%s" % recipe.entity_id
    title = "%s: %s" % (cookbook.name, recipe.name)

    # Info section
    edit_entity_link = "/editrecipe/%s" % recipe.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", "recipe_name", recipe.name),
        create_edit_info_dict("Category", "recipe_category", recipe.category),
        create_edit_info_dict("Priority", "recipe_priority", str(recipe.priority)),
        create_edit_info_dict("Has image", "recipe_has_image", str(recipe.has_image)),
        create_edit_info_dict("Notes", "recipe_notes", recipe.notes)
    ]

    delete_link = "/deleterecipe/%s" % recipe.entity_id
    delete_id = "recipe_delete"

    return render_template('edit_entity.html', **locals())


@app.route("/addentry", methods=["POST"])
def add_entry():
    entry = entry_manager.add_new_entity(
        int(request.form["entry_recipe_id"]), {
            Entry.DATE_HEADER: request.form["entry_date"],
            Entry.MIRIAM_RATING_HEADER: request.form["entry_miriam_rating"],
            Entry.JAMES_RATING_HEADER: request.form["entry_james_rating"],
            Entry.MIRIAM_COMMENTS_HEADER: request.form["entry_miriam_comments"],
            Entry.JAMES_COMMENTS_HEADER: request.form["entry_james_comments"]})
    return redirect(url_for("render_recipe", entity_id=entry.parent_id))


@app.route("/editentry/<int:entity_id>", methods=["POST"])
def edit_entry(entity_id: int):
    entry_manager.modify_entity(
        entity_id, {
            Entry.DATE_HEADER: request.form["entry_date"],
            Entry.MIRIAM_RATING_HEADER: request.form["entry_miriam_rating"],
            Entry.JAMES_RATING_HEADER: request.form["entry_james_rating"],
            Entry.MIRIAM_COMMENTS_HEADER: request.form["entry_miriam_comments"],
            Entry.JAMES_COMMENTS_HEADER: request.form["entry_james_comments"]})
    return redirect(url_for("render_entry", entity_id=entity_id))


@app.route("/deleteentry/<int:entity_id>", methods=["POST"])
def delete_entry(entity_id: int):
    if request.form["entry_delete"] != "delete":
        return redirect(url_for("render_edit_entry", entity_id=entity_id))

    recipe_id = entry_manager.get_entity(entity_id).parent_id
    entry_manager.delete_entity(entity_id)
    return redirect(url_for("render_recipe", entity_id=recipe_id))


@app.route("/entry/view/<int:entity_id>")
def render_entry(entity_id: int):
    has_info_template = True
    has_children_list_template = False
    has_add_child_template = False

    debug_mode = settings.debug_mode
    entry = entry_manager.get_entity(entity_id)
    recipe = entry.parent

    # Title section
    back_link = "/recipe/view/%s" % recipe.entity_id
    back_text = "Back to %s page" % recipe.name
    edit_link = "/entry/edit/%s" % entry.entity_id
    title = "Entry for: %s" % recipe.name

    # Info section
    info_dicts = [
        create_info_dict("Date", entry.date_string()),
        create_info_dict("Miriam's rating", str(entry.miriam_rating)),
        create_info_dict("James' rating", str(entry.james_rating)),
        create_info_dict("Miriam's comments", entry.miriam_comments),
        create_info_dict("James' comments", entry.james_comments),
    ]

    return render_template('view_entity.html', **locals())


@app.route("/entry/edit/<int:entity_id>")
def render_edit_entry(entity_id: int):
    debug_mode = settings.debug_mode
    entry = entry_manager.get_entity(entity_id)
    recipe = entry.parent

    # Title section
    back_link = "/recipe/view/%s" % recipe.entity_id
    back_text = "Back to %s page" % recipe.name
    view_link = "/entry/view/%s" % entry.entity_id
    title = "Entry for: %s" % recipe.name

    # Info section
    edit_entity_link = "/editentry/%s" % entry.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Date", "entry_date", entry.date_string()),
        create_edit_info_dict("Miriam's rating", "entry_miriam_rating", entry.miriam_rating),
        create_edit_info_dict("James' rating", "entry_james_rating", entry.james_rating),
        create_edit_info_dict("Miriam's comments", "entry_miriam_comments", entry.miriam_comments),
        create_edit_info_dict("James' comments", "entry_james_comments", entry.james_comments)
    ]

    delete_link = "/deleteentry/%s" % entry.entity_id
    delete_id = "entry_delete"

    return render_template('edit_entity.html', **locals())


@app.route('/serveimage/<path:filename>')
def serve_image(filename):
    return send_from_directory(settings.recipe_app_directory + "RecipeImages/",
                               filename, as_attachment=True)


def create_info_dict(name: str, value: str):
    return {"name": name, "value": value}


def create_edit_info_dict(name: str, entity_id: str, value: str):
    return {"name": name, "entity_id": entity_id, "value": value}


def create_add_child_dict(name: str, child_id: str, value: str, placeholder: str):
    return {"name": name, "child_id": child_id, "value": value, "placeholder": placeholder}


def create_add_child_hidden_dict(child_id: str, value: str):
    return {"child_id": child_id, "value": value}


initialize_app()
"""
    TODO: Reincorporate this back into the view_entity page.
    <form action="/recipe/uploadimage/{{recipe.entity_id}}" method=post enctype=multipart/form-data>
      <tr>
        <td><input type="file" name="file"></td>
        <td><input type="submit" value="Upload">
      </tr>
    </form>
"""

@app.route("/addcity", methods=["POST"])
def add_city():
    city_manager.add_new_entity(None, {
        City.NAME_HEADER: request.form["city_name"],
        City.STATE_HEADER: request.form["city_state"],
        City.COUNTRY_HEADER: request.form["city_country"],
        City.NOTES_HEADER: request.form["city_notes"]})
    return redirect(url_for("render_cities"))


@app.route("/editcity/<int:entity_id>", methods=["POST"])
def edit_city(entity_id: int):
    city_manager.modify_entity(entity_id,
                               {
                                   City.NAME_HEADER: request.form["city_name"],
                                   City.STATE_HEADER: request.form["city_state"],
                                   City.COUNTRY_HEADER: request.form["city_country"],
                                   City.NOTES_HEADER: request.form["city_notes"]})
    return redirect(url_for("render_city", entity_id=entity_id))


@app.route("/deletecity/<int:entity_id>", methods=["POST"])
def delete_city(entity_id: int):
    if request.form["city_delete"] != "delete":
        return redirect(url_for("render_edit_city", entity_id=entity_id))

    city_manager.delete_entity(entity_id)
    return redirect(url_for("render_cities"))


@app.route("/city/view/<int:entity_id>")
def render_city(entity_id: int):
    has_info_template = True
    has_children_list_template = True
    has_add_child_template = True

    debug_mode = settings.debug_mode
    city = city_manager.get_entity(entity_id)

    # Title section
    back_link = "/cities"
    back_text = "Back to cities page"
    edit_link = "/city/edit/%s" % city.entity_id
    title = city.name

    info_dicts = [
        create_info_dict("State", city.state),
        create_info_dict("Country", city.country),
        create_info_dict("Notes", city.notes)
    ]

    # Children list section
    child_table_headers = [
        "Name", "Num dishes tried", "Best rating", "Category"]
    child_table_values = []

    for restaurant in city.restaurants_by_best_rating_descending():
        child_table_values.append({
            "link": "/restaurant/view/%s" % restaurant.entity_id,
            "row": [restaurant.name,
                    str(restaurant.get_num_dishes_tried()),
                    str(restaurant.get_best_rating()),
                    restaurant.category]})

    # Add child section
    add_child_link = "/addrestaurant"
    add_child_title = "Add Restaurant"

    add_child_dicts = [
        create_add_child_dict("Name", "restaurant_name", "", "Name"),
        create_add_child_dict("Category", "restaurant_category", "", "Category"),
        create_add_child_dict("Notes", "restaurant_notes", "", "Notes")]

    add_child_hidden_dicts = [
        create_add_child_hidden_dict("restaurant_city_id", str(city.entity_id))
    ]

    return render_template('view_entity.html', **locals())


@app.route("/city/edit/<int:entity_id>")
def render_edit_city(entity_id: int):
    debug_mode = settings.debug_mode
    city = city_manager.get_entity(entity_id)

    # Title section
    back_link = "/"
    back_text = "Back to main page"
    view_link = "/city/view/%s" % city.entity_id
    title = city.name

    # Info section
    edit_entity_link = "/editcity/%s" % city.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", "city_name", city.name),
        create_edit_info_dict("State", "city_state", city.state),
        create_edit_info_dict("Country", "city_country", city.country),
        create_edit_info_dict("Notes", "city_notes", city.notes)
    ]

    delete_link = "/deletecity/%s" % city.entity_id
    delete_id = "city_delete"

    return render_template('edit_entity.html', **locals())


@app.route("/addrestaurant", methods=["POST"])
def add_restaurant():
    restaurant = restaurant_manager.add_new_entity(
        int(request.form["restaurant_city_id"]), {
            Restaurant.NAME_HEADER: request.form["restaurant_name"],
            Restaurant.CATEGORY_HEADER: request.form["restaurant_category"],
            Restaurant.NOTES_HEADER: request.form["restaurant_notes"]})
    return redirect(url_for("render_city", entity_id=restaurant.parent_id))


@app.route("/editrestaurant/<int:entity_id>", methods=["POST"])
def edit_restaurant(entity_id: int):
    restaurant_manager.modify_entity(
        entity_id, {
            Restaurant.NAME_HEADER: request.form["restaurant_name"],
            Restaurant.CATEGORY_HEADER: request.form["restaurant_category"],
            Restaurant.NOTES_HEADER: request.form["restaurant_notes"]})
    return redirect(url_for("render_restaurant", entity_id=entity_id))


@app.route("/deleterestaurant/<int:entity_id>", methods=["POST"])
def delete_restaurant(entity_id: int):
    if request.form["restaurant_delete"] != "delete":
        return redirect(url_for("render_edit_restaurant", entity_id=entity_id))

    city_id = restaurant_manager.get_entity(entity_id).parent_id
    restaurant_manager.delete_entity(entity_id)
    return redirect(url_for("render_city", entity_id=city_id))


@app.route("/restaurant/view/<int:entity_id>")
def render_restaurant(entity_id: int):
    has_info_template = True
    has_children_list_template = True
    has_add_child_template = True

    debug_mode = settings.debug_mode
    restaurant = restaurant_manager.get_entity(entity_id)
    city = restaurant.parent

    # Title section
    back_link = "/city/view/%s" % city.entity_id
    back_text = "Back to %s page" % city.name
    edit_link = "/restaurant/edit/%s" % restaurant.entity_id
    title = "%s: %s" % (city.name, restaurant.name)

    # Info section
    info_dicts = [
        create_info_dict("Best rating", str(restaurant.get_best_rating())),
        create_info_dict("Category", str(restaurant.category)),
        create_info_dict("Notes", restaurant.notes)
    ]

    # Children list section
    child_table_headers = [
        "Name", "Num times tried", "Best rating", "Latest rating", "Priority", "Category"]
    child_table_values = []

    for dish in restaurant.dishes_by_best_rating_descending():
        child_table_values.append({
            "link": "/dish/view/%s" % dish.entity_id,
            "row": [dish.name,
                    str(dish.get_num_times_tried()),
                    str(dish.get_best_rating()),
                    str(dish.get_latest_rating()),
                    str(dish.priority),
                    dish.category]})

    # Add child section
    add_child_link = "/adddish"
    add_child_title = "Add Dish"

    add_child_dicts = [
        create_add_child_dict("Name", "dish_name", "", "Name"),
        create_add_child_dict("Category", "dish_category", "", "Category"),
        create_add_child_dict("Priority", "dish_priority", "", "Priority"),
        create_add_child_dict("Notes", "dish_notes", "", "Notes")]

    add_child_hidden_dicts = [
        create_add_child_hidden_dict("dish_restaurant_id", str(restaurant.entity_id))
    ]

    return render_template('view_entity.html', **locals())


@app.route("/restaurant/edit/<int:entity_id>")
def render_edit_restaurant(entity_id: int):
    debug_mode = settings.debug_mode
    restaurant = restaurant_manager.get_entity(entity_id)
    city = restaurant.parent

    # Title section
    back_link = "/city/view/%s" % city.entity_id
    back_text = "Back to %s page" % city.name
    view_link = "/restaurant/view/%s" % restaurant.entity_id
    title = "%s: %s" % (city.name, restaurant.name)

    # Info section
    edit_entity_link = "/editrestaurant/%s" % restaurant.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", "restaurant_name", restaurant.name),
        create_edit_info_dict("Category", "restaurant_category", restaurant.category),
        create_edit_info_dict("Notes", "restaurant_notes", restaurant.notes)
    ]

    delete_link = "/deleterestaurant/%s" % restaurant.entity_id
    delete_id = "restaurant_delete"

    return render_template('edit_entity.html', **locals())


@app.route("/adddish", methods=["POST"])
def add_dish():
    dish = dish_manager.add_new_entity(
        int(request.form["dish_restaurant_id"]), {
            Dish.NAME_HEADER: request.form["dish_name"],
            Dish.PRIORITY_HEADER: request.form["dish_priority"],
            Dish.HAS_IMAGE_HEADER: "False",
            Dish.CATEGORY_HEADER: request.form["dish_category"],
            Dish.NOTES_HEADER: request.form["dish_notes"]})
    return redirect(url_for("render_restaurant", entity_id=dish.parent_id))


@app.route("/dish/uploadimage/<int:entity_id>", methods=["POST", "GET"])
def upload_dish_image(entity_id: int):
    dish_manager.upload_dish_image(entity_id, request.files['file'])
    return redirect(url_for("render_dish", entity_id=entity_id))


@app.route("/editdish/<int:entity_id>", methods=["POST"])
def edit_dish(entity_id: int):
    dish_manager.modify_entity(
        entity_id, {
            Dish.NAME_HEADER: request.form["dish_name"],
            Dish.PRIORITY_HEADER: request.form["dish_priority"],
            Dish.HAS_IMAGE_HEADER: request.form["dish_has_image"],
            Dish.CATEGORY_HEADER: request.form["dish_category"],
            Dish.NOTES_HEADER: request.form["dish_notes"]})
    return redirect(url_for("render_dish", entity_id=entity_id))


@app.route("/deletedish/<int:entity_id>", methods=["POST"])
def delete_dish(entity_id: int):
    if request.form["dish_delete"] != "delete":
        return redirect(url_for("render_edit_dish", entity_id=entity_id))

    restaurant_id = dish_manager.get_entity(entity_id).parent_id
    dish_manager.delete_entity(entity_id)
    return redirect(url_for("render_restaurant", entity_id=restaurant_id))


@app.route("/dish/view/<int:entity_id>")
def render_dish(entity_id: int):
    has_info_template = True
    has_children_list_template = True
    has_add_child_template = True

    debug_mode = settings.debug_mode
    dish = dish_manager.get_entity(entity_id)
    restaurant = dish.parent

    # Title section
    back_link = "/restaurant/view/%s" % restaurant.entity_id
    back_text = "Back to %s page" % restaurant.name
    edit_link = "/dish/edit/%s" % dish.entity_id
    title = "%s: %s" % (restaurant.name, dish.name)

    # Info section
    info_image_name = None
    if dish.has_image:
        info_image_name = "/serveimage/%s.jpg" % dish.entity_id

    info_dicts = [
        create_info_dict("Best rating", str(dish.get_best_rating())),
        create_info_dict("Latest rating", str(dish.get_latest_rating())),
        create_info_dict("Num times made", str(dish.get_num_times_tried())),
        create_info_dict("Category", str(dish.category)),
        create_info_dict("Priority", str(dish.priority)),
        create_info_dict("Notes", dish.notes)
    ]

    # Children list section
    child_table_headers = [
        "Date", "Overall Rating", "Miriam's Rating", "Miriam's Comments", "James' Rating", "James' Comments"]
    child_table_values = []

    for entry in dish.dish_entries_by_date_descending():
        child_table_values.append({
            "link": "/dishentry/view/%s" % entry.entity_id,
            "row": [entry.date_string(), entry.get_overall_rating(), entry.miriam_rating, entry.miriam_comments,
             entry.james_rating, entry.james_comments]})

    # Add child section
    add_child_link = "/adddishentry"
    add_child_title = "Add Entry"

    add_child_dicts = [
        create_add_child_dict("Date", "dish_entry_date", datetime.datetime.today().strftime('%Y-%m-%d'), ""),
        create_add_child_dict("Miriam's Rating", "dish_entry_miriam_rating", "", "Miriam's rating"),
        create_add_child_dict("Miriam's Comments", "dish_entry_miriam_comments", "", "Miriam's comments"),
        create_add_child_dict("James' Rating", "dish_entry_james_rating", "", "James' rating"),
        create_add_child_dict("James' Comments", "dish_entry_james_comments", "", "James' comments"),
    ]

    add_child_hidden_dicts = [
        create_add_child_hidden_dict("dish_entry_dish_id", str(dish.entity_id))
    ]

    return render_template('view_entity.html', **locals())


@app.route("/dish/edit/<int:entity_id>")
def render_edit_dish(entity_id: int):
    debug_mode = settings.debug_mode
    dish = dish_manager.get_entity(entity_id)
    restaurant = dish.parent

    # Title section
    back_link = "/restaurant/view/%s" % restaurant.entity_id
    back_text = "Back to %s page" % restaurant.name
    view_link = "/dish/view/%s" % dish.entity_id
    title = "%s: %s" % (restaurant.name, dish.name)

    # Info section
    edit_entity_link = "/editdish/%s" % dish.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", "dish_name", dish.name),
        create_edit_info_dict("Category", "dish_category", dish.category),
        create_edit_info_dict("Priority", "dish_priority", str(dish.priority)),
        create_edit_info_dict("Has image", "dish_has_image", str(dish.has_image)),
        create_edit_info_dict("Notes", "dish_notes", dish.notes)
    ]

    delete_link = "/deletedish/%s" % dish.entity_id
    delete_id = "dish_delete"

    return render_template('edit_entity.html', **locals())


@app.route("/adddishentry", methods=["POST"])
def add_dish_entry():
    dish_entry = dish_entry_manager.add_new_entity(
        int(request.form["dish_entry_dish_id"]), {
            Entry.DATE_HEADER: request.form["dish_entry_date"],
            Entry.MIRIAM_RATING_HEADER: request.form["dish_entry_miriam_rating"],
            Entry.JAMES_RATING_HEADER: request.form["dish_entry_james_rating"],
            Entry.MIRIAM_COMMENTS_HEADER: request.form["dish_entry_miriam_comments"],
            Entry.JAMES_COMMENTS_HEADER: request.form["dish_entry_james_comments"]})
    return redirect(url_for("render_dish", entity_id=dish_entry.parent_id))


@app.route("/editdishentry/<int:entity_id>", methods=["POST"])
def edit_dish_entry(entity_id: int):
    dish_entry_manager.modify_entity(
        entity_id, {
            Entry.DATE_HEADER: request.form["dish_entry_date"],
            Entry.MIRIAM_RATING_HEADER: request.form["dish_entry_miriam_rating"],
            Entry.JAMES_RATING_HEADER: request.form["dish_entry_james_rating"],
            Entry.MIRIAM_COMMENTS_HEADER: request.form["dish_entry_miriam_comments"],
            Entry.JAMES_COMMENTS_HEADER: request.form["dish_entry_james_comments"]})
    return redirect(url_for("render_dish_entry", entity_id=entity_id))


@app.route("/deletedishentry/<int:entity_id>", methods=["POST"])
def delete_dish_entry(entity_id: int):
    if request.form["dish_entry_delete"] != "delete":
        return redirect(url_for("render_edit_dish_entry", entity_id=entity_id))

    dish_id = dish_entry_manager.get_entity(entity_id).parent_id
    dish_entry_manager.delete_entity(entity_id)
    return redirect(url_for("render_dish", entity_id=dish_id))


@app.route("/dishentry/view/<int:entity_id>")
def render_dish_entry(entity_id: int):
    has_info_template = True
    has_children_list_template = False
    has_add_child_template = False

    debug_mode = settings.debug_mode
    dish_entry = dish_entry_manager.get_entity(entity_id)
    recipe = dish_entry.parent

    # Title section
    back_link = "/dish/view/%s" % recipe.entity_id
    back_text = "Back to %s page" % recipe.name
    edit_link = "/dishentry/edit/%s" % dish_entry.entity_id
    title = "Entry for: %s" % recipe.name

    # Info section
    info_dicts = [
        create_info_dict("Date", dish_entry.date_string()),
        create_info_dict("Miriam's rating", str(dish_entry.miriam_rating)),
        create_info_dict("James' rating", str(dish_entry.james_rating)),
        create_info_dict("Miriam's comments", dish_entry.miriam_comments),
        create_info_dict("James' comments", dish_entry.james_comments),
    ]

    return render_template('view_entity.html', **locals())


@app.route("/dishentry/edit/<int:entity_id>")
def render_edit_dish_entry(entity_id: int):
    debug_mode = settings.debug_mode
    dish_entry = dish_entry_manager.get_entity(entity_id)
    dish = dish_entry.parent

    # Title section
    back_link = "/dish/view/%s" % dish.entity_id
    back_text = "Back to %s page" % dish.name
    view_link = "/dishentry/view/%s" % dish_entry.entity_id
    title = "Entry for: %s" % dish.name

    # Info section
    edit_entity_link = "/editdishentry/%s" % dish_entry.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Date", "dish_entry_date", dish_entry.date_string()),
        create_edit_info_dict("Miriam's rating", "dish_entry_miriam_rating", dish_entry.miriam_rating),
        create_edit_info_dict("James' rating", "dish_entry_james_rating", dish_entry.james_rating),
        create_edit_info_dict("Miriam's comments", "dish_entry_miriam_comments", dish_entry.miriam_comments),
        create_edit_info_dict("James' comments", "dish_entry_james_comments", dish_entry.james_comments)
    ]

    delete_link = "/deletedishentry/%s" % dish_entry.entity_id
    delete_id = "dish_entry_delete"

    return render_template('edit_entity.html', **locals())
