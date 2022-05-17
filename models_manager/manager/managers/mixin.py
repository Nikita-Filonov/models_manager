from models_manager.manager.managers.database import DatabaseManager
from models_manager.manager.managers.json import JsonManager
from models_manager.manager.managers.schema import SchemaManager


class ManagerMixin(DatabaseManager, JsonManager, SchemaManager):
    pass
