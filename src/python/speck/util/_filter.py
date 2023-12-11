import inspect


def filter_kwargs(func, all_kwargs, exclude=[]):
    func_signature = inspect.signature(func)
    valid_params = set(func_signature.parameters)
    filtered_kwargs = {
        k: v for k, v in all_kwargs.items() if k in valid_params and k not in exclude
    }
    return filtered_kwargs
