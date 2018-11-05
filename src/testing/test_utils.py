from typing import Tuple, List, Dict
from src.settings.settings import Settings
from src.entities.cookbook_manager import CookbookManager
from src.entities.recipe_manager import RecipeManager
from src.entities.entry_manager import EntryManager
from src.entities.entity import Entity
from src.entities.recipe import Recipe
from src.entities.cookbook import Cookbook
from src.entities.entry import Entry


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


def default_entry_dict_with_overrides(overrides: Dict[str, str] = {}) -> Dict[str, str]:
    entry_dict = {
        Entry.DATE_HEADER: "2018-06-01",
        Entry.MIRIAM_RATING_HEADER: "8.0",
        Entry.JAMES_RATING_HEADER: "7.0",
        Entry.MIRIAM_COMMENTS_HEADER: "default miriam comments",
        Entry.JAMES_COMMENTS_HEADER: "default james comments"
    }
    entry_dict.update(overrides)
    return entry_dict


def default_recipe_dict_with_overrides(overrides: Dict[str, str] = {}) -> Dict[str, str]:
    recipe_dict = {
        Recipe.NAME_HEADER: "default name",
        Recipe.PRIORITY_HEADER: "2",
        Entity.HAS_IMAGE_HEADER: "False",
        Recipe.CATEGORY_HEADER: "default category",
        Recipe.NOTES_HEADER: "default notes"
    }
    recipe_dict.update(overrides)
    return recipe_dict


def default_cookbook_dict_with_overrides(overrides: Dict[str, str] = {}) -> Dict[str, str]:
    cookbook_dict = {
        Cookbook.NAME_HEADER: "default name",
        Cookbook.NOTES_HEADER: "default notes"
    }
    cookbook_dict.update(overrides)
    return cookbook_dict
