from datetime import datetime, date, time, timedelta
from http import HTTPStatus

TYPE_NAMES = {
    HTTPStatus: 'integer',
    dict: 'object',
    str: 'string',
    int: 'number',
    float: 'number',
    list: 'array',
    bool: 'boolean',
    None: 'null',
    tuple: 'array',
    datetime: 'string',
    date: 'string',
    time: 'string',
    timedelta: 'string'
}
