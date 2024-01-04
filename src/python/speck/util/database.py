def db_get_format(kwargs):
    kwargs, version = db_convert_format(kwargs)
    return kwargs


def db_convert_format(kwargs) -> (dict, str):
    return kwargs, "v1"
