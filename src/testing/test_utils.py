from typing import Tuple
from src.settings.settings import Settings
from src.entities.cookbook_manager import CookbookManager
from src.entities.recipe_manager import RecipeManager
from src.entities.entry_manager import EntryManager


def initialize_test_environment() -> Tuple[CookbookManager, RecipeManager, EntryManager, Settings]:
    settings = Settings()
    settings.recipe_app_directory = "src/test_files/input/"
    cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager(settings)
    recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, settings)
    entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, settings)
    settings.recipe_app_directory = "src/test_files/output/"
    return cookbook_manager, recipe_manager, entry_manager, settings
