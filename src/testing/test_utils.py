from typing import Tuple, List
from src.settings.settings import Settings
from src.entities.cookbook_manager import CookbookManager
from src.entities.recipe_manager import RecipeManager
from src.entities.entry_manager import EntryManager
from src.entities.entity import Entity


def initialize_test_environment() -> Tuple[CookbookManager, RecipeManager, EntryManager, Settings]:
    settings = Settings()
    settings.recipe_app_directory = "src/test_files/input/"
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
    # TODO: Make settings take in both an input and output directory.
    settings.recipe_app_directory = "src/test_files/output/"
    return cookbook_manager, recipe_manager, entry_manager, settings


def print_entities(entities: List[Entity]):
    for entity in entities:
        print(str(entity))
