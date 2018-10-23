from entities.recipe import Recipe

RECIPES_FILE = "/home/james/Dropbox/RecipeApp/recipes.txt"


class RecipeManager:

    def __init__(self):
        self._recipes = {}

    @staticmethod
    def create_and_initialize_recipe_manager(filename: str=RECIPES_FILE):
        recipe_manager = RecipeManager()
        recipe_file = open(filename, "r")
        for recipe_line in recipe_file:
            if recipe_line.strip("\n"):
                recipe = Recipe.from_line(recipe_line)
                recipe_manager.add_existing_recipe(recipe)
        recipe_file.close()
        return recipe_manager

    # Adds recipes that already have an id.
    def add_existing_recipe(self, recipe: Recipe):
        assert recipe.id is not None, "Recipe id should not be None"
        self._recipes[recipe.id] = recipe

    def add_new_recipe(self, recipe: Recipe, filename: str=RECIPES_FILE):
        assert recipe.id is None, "Recipe id should be None"
        recipe_id = self._generate_recipe_id()
        recipe.id = recipe_id
        self._recipes[recipe_id] = recipe
        self._write_recipes_to_file(filename)

    def _write_recipes_to_file(self, filename: str):
        with open(filename, "w") as f:
            for recipe in sorted(self._recipes.values(), key=lambda recipe: recipe.id):
                f.write(recipe.to_line())
            f.write("\n")

    def _generate_recipe_id(self):
        i = 1
        while i in self._recipes:
            i += 1
        return i

    def get_recipes(self):
        return sorted(self._recipes.values(), key=lambda recipe: recipe.name.lower())

    def get_recipes_for_cookbook(self, id: int):
        recipes = self._recipes.values()
        recipes = filter(lambda recipe: recipe.cookbook_id == id, recipes)
        return sorted(recipes, key=lambda recipe: recipe.name.lower())

    def get_recipe(self, id: int):
        return self._recipes[id]
