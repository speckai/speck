import inspect


def filter_kwargs(func, all_kwargs):
    func_signature = inspect.signature(func)
    valid_params = set(func_signature.parameters)
    filtered_kwargs = {k: v for k, v in all_kwargs.items() if k in valid_params}
    return filtered_kwargs
