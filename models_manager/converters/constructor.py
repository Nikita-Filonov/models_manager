from models_manager.converters.converters import get_imports, get_field, get_class, str_generator


def construct_class(name, json: dict):
    if not isinstance(json, dict):
        raise NotImplementedError('To generate model class provide "json" argument as dictionary')

    default_class = get_class(name, json)

    fields = [get_field(json=key, default=value) for key, value in json.items()]
    joined_fields = '\n'.join(fields)
    imports = get_imports()

    return f"{imports}{default_class}\n{joined_fields}{str_generator(name, json)}"
