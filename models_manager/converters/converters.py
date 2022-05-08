import json as json_lib

from models_manager.utils import prettify_json


def get_imports():
    return 'from models_manager import Model, Field\n\n\n'


def get_field(json, default):
    safe_default = default

    if type(safe_default) in (str, dict, list):
        safe_default = json_lib.dumps(safe_default)

    if type(safe_default) in (bool,):
        safe_default = 'True' if safe_default else 'False'

    return f"\t{json} = Field(json='{json}', default={safe_default}, category={type(default).__name__})"


def get_class(name, json):
    default_class = f'class {name}(Model):' \
                    f'\n\t"""' \
                    f'\n\tThe "{name}" object models which describes following json:' \
                    f'\n\t{prettify_json(json)} ' \
                    f'\n\t"""\n'
    return default_class.replace('}', '\t}')


def str_generator(name, json):
    identity = next(filter(lambda j: (j[0].lower().startswith('id') or j[0].lower().endswith('id')), json.items()))

    if identity is not None:
        identity_name, _ = identity
        return '\n\n\tdef str(self):\n\t\treturn f"<%s: %s>"' % (name, "{self.%s.value}" % identity_name)

    return '\n\n\tdef str(self):\n\t\treturn f"<%s>"' % name
