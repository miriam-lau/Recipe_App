from flask import Flask, redirect, render_template, request, url_for, send_from_directory, jsonify
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
from typing import Optional


app = Flask(__name__)
cookbook_manager: CookbookManager = None
recipe_manager: RecipeManager = None
entry_manager: EntryManager = None
city_manager: CityManager = None
restaurant_manager: RestaurantManager = None
dish_manager: DishManager = None
dish_entry_manager: DishEntryManager = None
settings: Settings = None


DELETE_PARAM = "delete"
NON_WHITESPACE_PATTERN = "required pattern=.*\S+.*"


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


@app.route("/add/<entity_type>/<int:entity_id>", methods=["POST"])
def add_entity(entity_type: str, entity_id: int):
    entity_manager = None
    redirect_url = None
    if entity_type == "cookbook":
        entity_manager = cookbook_manager
        redirect_url = "render_cookbooks"
    elif entity_type == "recipe":
        entity_manager = recipe_manager
        redirect_url = "render_cookbook"
    elif entity_type == "entry":
        entity_manager = entry_manager
        redirect_url = "render_recipe"
    elif entity_type == "city":
        entity_manager = city_manager
        redirect_url = "render_cities"
    elif entity_type == "restaurant":
        entity_manager = restaurant_manager
        redirect_url = "render_city"
    elif entity_type == "dish":
        entity_manager = dish_manager
        redirect_url = "render_restaurant"
    elif entity_type == "dishentry":
        entity_manager = dish_entry_manager
        redirect_url = "render_dish"
    entity_manager.add_new_entity(entity_id, request.form.to_dict())
    return redirect(url_for(redirect_url, entity_id=entity_id))


@app.route("/edit/<entity_type>/<int:entity_id>", methods=["POST"])
def edit_entity(entity_type: str, entity_id: int):
    entity_manager = None
    redirect_url = None
    if entity_type == "cookbook":
        entity_manager = cookbook_manager
        redirect_url = "render_cookbook"
    elif entity_type == "recipe":
        entity_manager = recipe_manager
        redirect_url = "render_recipe"
    elif entity_type == "entry":
        entity_manager = entry_manager
        redirect_url = "render_entry"
    elif entity_type == "city":
        entity_manager = city_manager
        redirect_url = "render_city"
    elif entity_type == "restaurant":
        entity_manager = restaurant_manager
        redirect_url = "render_restaurant"
    elif entity_type == "dish":
        entity_manager = dish_manager
        redirect_url = "render_dish"
    elif entity_type == "dishentry":
        entity_manager = dish_entry_manager
        redirect_url = "render_dish_entry"
    entity_manager.modify_entity(entity_id, request.form.to_dict())
    return redirect(url_for(redirect_url, entity_id=entity_id))


@app.route("/delete/<entity_type>/<int:entity_id>", methods=["POST"])
def delete_entity(entity_type, entity_id: int):
    entity_manager = None
    unsuccessful_redirect_url = None
    successful_redirect_url = None
    if entity_type == "cookbook":
        entity_manager = cookbook_manager
        unsuccessful_redirect_url = "render_edit_cookbook"
        successful_redirect_url = "render_cookbooks"
    elif entity_type == "recipe":
        entity_manager = recipe_manager
        unsuccessful_redirect_url = "render_edit_recipe"
        successful_redirect_url = "render_cookbook"
    elif entity_type == "entry":
        entity_manager = entry_manager
        unsuccessful_redirect_url = "render_edit_entry"
        successful_redirect_url = "render_recipe"
    elif entity_type == "city":
        entity_manager = city_manager
        unsuccessful_redirect_url = "render_edit_city"
        successful_redirect_url = "render_cities"
    elif entity_type == "restaurant":
        entity_manager = restaurant_manager
        unsuccessful_redirect_url = "render_edit_restaurant"
        successful_redirect_url = "render_city"
    elif entity_type == "dish":
        entity_manager = dish_manager
        unsuccessful_redirect_url = "render_edit_dish"
        successful_redirect_url = "render_restaurant"
    elif entity_type == "dishentry":
        entity_manager = dish_entry_manager
        unsuccessful_redirect_url = "render_edit_dish_entry"
        successful_redirect_url = "render_dish"
    if request.form[DELETE_PARAM] != "delete":
        return redirect(url_for(unsuccessful_redirect_url, entity_id=entity_id))

    parent_id = entity_manager.get_entity(entity_id).parent_id
    entity_manager.delete_entity(entity_id)
    return redirect(url_for(successful_redirect_url, entity_id=parent_id))


@app.route("/recipe/uploadimage/<int:entity_id>", methods=["POST", "GET"])
def upload_recipe_image(entity_id: int):
    recipe_manager.upload_recipe_image(entity_id, request.files['file'])
    return redirect(url_for("render_recipe", entity_id=entity_id))


@app.route("/")
def render_main():
    debug_mode = settings.debug_mode
    return render_template('main.html', **locals())


@app.route("/scripts.js")
def render_scripts():
    return render_template('scripts.js', **locals())


@app.route("/cities")
def render_cities():
    debug_mode = settings.debug_mode
    cities = city_manager.get_sorted_cities()

    has_info_template = False
    has_children_list_template = True
    has_add_child_template = True

    back_link = "/"
    back_text = "Back to main page"

    # Title section
    title = "Cities"

    # Children list section
    child_table_headers = ["Name", "State", "Country", "Notes"]
    child_table_values = []

    for city in cities:
        child_table_values.append({
            "link": "/city/view/%s" % city.entity_id,
            "row": [city.name, city.state, city.country, city.notes]})

    # Add child section
    add_child_link = "/add/city/0"
    add_child_title = "Add City"

    add_child_dicts = [
        create_add_child_dict("Name", City.NAME_HEADER, "", "Name", NON_WHITESPACE_PATTERN),
        create_add_child_dict("State", City.STATE_HEADER, "", "State"),
        create_add_child_dict("Country", City.COUNTRY_HEADER, "", "Country"),
        create_add_child_dict("Notes", City.NOTES_HEADER, "", "Notes")
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
    add_child_link = "/add/cookbook/0"
    add_child_title = "Add Cookbook"

    add_child_dicts = [
        create_add_child_dict("Name", Cookbook.NAME_HEADER, "", "Cookbook name", NON_WHITESPACE_PATTERN),
        create_add_child_dict("Notes", Cookbook.NOTES_HEADER, "", "Cookbook notes")
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
    edit_entity_link = "/edit/cookbook/%s" % cookbook.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", Cookbook.NAME_HEADER, cookbook.name, NON_WHITESPACE_PATTERN),
        create_edit_info_dict("Notes", Cookbook.NOTES_HEADER, cookbook.notes)
    ]

    delete_link = "/delete/cookbook/%s" % cookbook.entity_id
    delete_entity_type = "cookbook"

    return render_template('edit_entity.html', **locals())


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
    add_child_link = "/add/recipe/%s" % entity_id
    add_child_title = "Add Recipe"

    add_child_dicts = [
        create_add_child_dict("Name", Recipe.NAME_HEADER, "", "Name", NON_WHITESPACE_PATTERN),
        create_add_child_dict("Category", Recipe.CATEGORY_HEADER, "", "Category"),
        create_add_child_dict("Priority", Recipe.PRIORITY_HEADER, "0", "", "required min=0 max=4 step=1 type=number"),
        create_add_child_dict("Notes", Recipe.NOTES_HEADER, "", "Notes")]

    return render_template('view_entity.html', **locals())


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
    add_child_link = "/add/entry/%s" % entity_id
    add_child_title = "Add Entry"

    add_child_dicts = [
        create_add_child_dict("Date", Entry.DATE_HEADER, datetime.datetime.today().strftime('%Y-%m-%d'), "", "required type=date"),
        create_add_child_dict("Miriam's Rating", Entry.MIRIAM_RATING_HEADER, "", "Miriam's rating",
                              "min=0 max=10 step=0.1 required type=number"),
        create_add_child_dict("Miriam's Comments", Entry.MIRIAM_COMMENTS_HEADER, "", "Miriam's comments"),
        create_add_child_dict("James' Rating", Entry.JAMES_RATING_HEADER, "", "James' rating",
                              "min=0 max=10 step=0.1 required type=number"),
        create_add_child_dict("James' Comments", Entry.JAMES_COMMENTS_HEADER, "", "James' comments"),
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
    edit_entity_link = "/edit/recipe/%s" % recipe.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", Recipe.NAME_HEADER, recipe.name, NON_WHITESPACE_PATTERN),
        create_edit_info_dict("Category", Recipe.CATEGORY_HEADER, recipe.category),
        create_edit_info_dict("Priority", Recipe.PRIORITY_HEADER, str(recipe.priority),
                              "required min=0 max=4 step=1 type=number"),
        create_edit_info_dict("Has image", Recipe.HAS_IMAGE_HEADER, str(recipe.has_image),
                              "required pattern=true|false|True|False"),
        create_edit_info_dict("Notes", Recipe.NOTES_HEADER, recipe.notes)
    ]

    delete_link = "/delete/recipe/%s" % recipe.entity_id
    delete_entity_type = "recipe"

    return render_template('edit_entity.html', **locals())


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
    edit_entity_link = "/edit/entry/%s" % entry.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Date", Entry.DATE_HEADER, entry.date_string(), "required type=date"),
        create_edit_info_dict("Miriam's rating", Entry.MIRIAM_RATING_HEADER, entry.miriam_rating,
                              "min=0 max=10 step=0.1 required type=number"),
        create_edit_info_dict("James' rating", Entry.JAMES_RATING_HEADER, entry.james_rating,
                              "min=0 max=10 step=0.1 required type=number"),
        create_edit_info_dict("Miriam's comments", Entry.MIRIAM_COMMENTS_HEADER, entry.miriam_comments),
        create_edit_info_dict("James' comments", Entry.JAMES_COMMENTS_HEADER, entry.james_comments)
    ]

    delete_link = "/delete/entry/%s" % entry.entity_id
    delete_entity_type = "entry"

    return render_template('edit_entity.html', **locals())


@app.route('/serveimage/<path:filename>')
def serve_image(filename):
    return send_from_directory(settings.recipe_app_directory + "RecipeImages/",
                               filename, as_attachment=True)


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
    add_child_link = "/add/restaurant/%s" % entity_id
    add_child_title = "Add Restaurant"

    add_child_dicts = [
        create_add_child_dict("Name", Restaurant.NAME_HEADER, "", "Name", NON_WHITESPACE_PATTERN),
        create_add_child_dict("Address", Restaurant.ADDRESS_HEADER, "", "Address"),
        create_add_child_dict("Category", Restaurant.CATEGORY_HEADER, "", "Category"),
        create_add_child_dict("Notes", Restaurant.NOTES_HEADER, "", "Notes")]

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
    edit_entity_link = "/edit/city/%s" % city.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", City.NAME_HEADER, city.name, NON_WHITESPACE_PATTERN),
        create_edit_info_dict("State", City.STATE_HEADER, city.state),
        create_edit_info_dict("Country", City.COUNTRY_HEADER, city.country),
        create_edit_info_dict("Notes", City.NOTES_HEADER, city.notes)
    ]

    delete_link = "/delete/city/%s" % city.entity_id
    delete_entity_type = "city"

    return render_template('edit_entity.html', **locals())


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
        create_info_dict("Address", str(restaurant.address)),
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
    add_child_link = "/add/dish/%s" % entity_id
    add_child_title = "Add Dish"

    add_child_dicts = [
        create_add_child_dict("Name", Dish.NAME_HEADER, "", "Name", NON_WHITESPACE_PATTERN),
        create_add_child_dict("Category", Dish.CATEGORY_HEADER, "", "Category"),
        create_add_child_dict("Priority", Dish.PRIORITY_HEADER, "", "Priority",
                              "required min=0 max=4 step=1 type=number"),
        create_add_child_dict("Notes", Dish.NOTES_HEADER, "", "Notes")]

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
    edit_entity_link = "/edit/restaurant/%s" % restaurant.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", Restaurant.NAME_HEADER, restaurant.name, NON_WHITESPACE_PATTERN),
        create_edit_info_dict("Address", Restaurant.ADDRESS_HEADER, restaurant.address, NON_WHITESPACE_PATTERN),
        create_edit_info_dict("Category", Restaurant.CATEGORY_HEADER, restaurant.category),
        create_edit_info_dict("Notes", Restaurant.NOTES_HEADER, restaurant.notes)
    ]

    delete_link = "/delete/restaurant/%s" % restaurant.entity_id
    delete_entity_type = "restaurant"

    return render_template('edit_entity.html', **locals())


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
    add_child_link = "/add/dishentry/%s" % entity_id
    add_child_title = "Add Entry"

    add_child_dicts = [
        create_add_child_dict("Date", DishEntry.DATE_HEADER, datetime.datetime.today().strftime('%Y-%m-%d'), "",
                              "required type=date"),
        create_add_child_dict("Miriam's Rating", DishEntry.MIRIAM_RATING_HEADER, "", "Miriam's rating",
                              "min=0 max=10 step=0.1 required type=number"),
        create_add_child_dict("Miriam's Comments", DishEntry.MIRIAM_COMMENTS_HEADER, "", "Miriam's comments"),
        create_add_child_dict("James' Rating", DishEntry.JAMES_RATING_HEADER, "", "James' rating",
                              "min=0 max=10 step=0.1 required type=number"),
        create_add_child_dict("James' Comments", DishEntry.JAMES_COMMENTS_HEADER, "", "James' comments"),
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
    edit_entity_link = "/edit/dish/%s" % dish.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Name", Dish.NAME_HEADER, dish.name, NON_WHITESPACE_PATTERN),
        create_edit_info_dict("Category", Dish.CATEGORY_HEADER, dish.category),
        create_edit_info_dict("Priority", Dish.PRIORITY_HEADER, str(dish.priority),
                              "required min=0 max=4 step=1 type=number"),
        create_edit_info_dict("Has image", Dish.HAS_IMAGE_HEADER, str(dish.has_image),
                              "required pattern=true|false|True|False"),
        create_edit_info_dict("Notes", Dish.NOTES_HEADER, dish.notes)
    ]

    delete_link = "/delete/dish/%s" % dish.entity_id
    delete_entity_type = "dish"

    return render_template('edit_entity.html', **locals())


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
    edit_entity_link = "/edit/dishentry/%s" % dish_entry.entity_id

    edit_info_dicts = [
        create_edit_info_dict("Date", DishEntry.DATE_HEADER, dish_entry.date_string(), "required type=date"),
        create_edit_info_dict("Miriam's rating", DishEntry.MIRIAM_RATING_HEADER, dish_entry.miriam_rating,
                              "min=0 max=10 step=0.1 required type=number"),
        create_edit_info_dict("James' rating", DishEntry.JAMES_RATING_HEADER, dish_entry.james_rating,
                              "min=0 max=10 step=0.1 required type=number"),
        create_edit_info_dict("Miriam's comments", DishEntry.MIRIAM_COMMENTS_HEADER, dish_entry.miriam_comments),
        create_edit_info_dict("James' comments", DishEntry.JAMES_COMMENTS_HEADER, dish_entry.james_comments)
    ]

    delete_link = "/delete/dishentry/%s" % dish_entry.entity_id
    delete_entity_type = "dish entry"

    return render_template('edit_entity.html', **locals())


@app.route("/dish/uploadimage/<int:entity_id>", methods=["POST", "GET"])
def upload_dish_image(entity_id: int):
    dish_manager.upload_dish_image(entity_id, request.files['file'])
    return redirect(url_for("render_dish", entity_id=entity_id))


@app.route("/search_recipes")
def render_search_recipe():
    debug_mode = settings.debug_mode

    recipes = recipe_manager.get_entities()

    recipe_dicts = []

    for recipe in recipes:
        recipe_dict = recipe.to_dict()
        recipe_dict["num_times_made"] = recipe.get_num_times_made()
        recipe_dict["best_rating"] = recipe.get_best_rating()
        recipe_dict["latest_rating"] = recipe.get_latest_rating()
        recipe_dict["cookbook_name"] = recipe.parent.name
        recipe_dicts.append(recipe_dict)

    return render_template('search_recipes.html', **locals())


@app.route("/search_dishes")
def render_search_dish():
    debug_mode = settings.debug_mode

    dishes = dish_manager.get_entities()

    dish_dicts = []

    for dish in dishes:
        dish_dict = dish.to_dict()
        dish_dict["num_times_tried"] = dish.get_num_times_tried()
        dish_dict["best_rating"] = dish.get_best_rating()
        dish_dict["latest_rating"] = dish.get_latest_rating()
        dish_dict["restaurant_name"] = dish.parent.name
        dish_dict["city_name"] = dish.parent.parent.name
        dish_dicts.append(dish_dict)

    return render_template('search_dishes.html', **locals())


@app.route("/search_restaurants")
def render_search_restaurants():
    debug_mode = settings.debug_mode

    restaurants = restaurant_manager.get_entities()

    restaurant_dicts = []

    for restaurant in restaurants:
        restaurant_dict = restaurant.to_dict()
        restaurant_dict["best_rating"] = restaurant.get_best_rating()
        restaurant_dict["city_name"] = restaurant.parent.name
        restaurant_dicts.append(restaurant_dict)

    return render_template('search_restaurants.html', **locals())


def create_info_dict(name: str, value: str):
    return {"name": name, "value": value}


def create_edit_info_dict(name: str, entity_id: str, value: str, input_attributes: Optional[str]=None):
    return {
        "name": name,
        "entity_id": entity_id,
        "value": value,
        "input_attributes": input_attributes
    }


def create_add_child_dict(name: str, child_id: str, value: str, placeholder: str, input_attributes: Optional[str]=None):
    return {
        "name": name,
        "child_id": child_id,
        "value": value,
        "placeholder": placeholder,
        "input_attributes": input_attributes
    }


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

