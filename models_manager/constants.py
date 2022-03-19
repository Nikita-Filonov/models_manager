from http import HTTPStatus

TYPE_NAMES = {
    HTTPStatus: 'integer',
    dict: 'object',
    str: 'string',
    int: 'number',
    float: 'number',
    list: 'array',
    bool: 'boolean',
    None: 'null'
}
