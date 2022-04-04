from models_manager.manager.field.typing import GenericCategories, GenericTypes


def get_enum_value(category: GenericCategories, default: GenericTypes):
    return category.get_value(default) if hasattr(category, 'get_value') else default.value
