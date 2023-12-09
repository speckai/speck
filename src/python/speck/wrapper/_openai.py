import logging

from openai import OpenAI as _OpenAI
from openai import Stream as _Stream

from ..util._wrapper import wrap_method

logger = logging.getLogger(__name__)
logger.info = print


def wrapper(original_method, *args, **kwargs):
    """
    Example of a wrapper function that can be used with add_method_wrapper.

    Args:
        original_method: The original method to be wrapped.
        *args, **kwargs: Arguments and keyword arguments for the original method.

    Returns:
        The result of the original method call.
    """
    logger.info(f"Before calling {original_method.__name__}")
    result = original_method(*args, **kwargs)
    logger.info(f"After calling {original_method.__name__}")
    return result


def chat_wrapper(original_method, *args, **kwargs):
    """
    Example of a wrapper function that can be used with add_method_wrapper.

    Args:
        original_method: The original method to be wrapped.
        *args, **kwargs: Arguments and keyword arguments for the original method.

    Returns:
        The result of the original method call.
    """
    model = kwargs.get("model", None)
    stream = kwargs.get("stream", False)

    if model is not None and ":" in model:
        model = model.split(":")[1]
        # Todo: convert other model responses to OpenAI response format

    logger.info(f"Call {original_method.__name__} with model {model}")
    if stream:
        print("Stream called!")
        stream = original_method(*args, **kwargs)
        # Todo: wrap the Stream class
        # Best current way to do this is to convert our Stream class to an OpenAI Stream class
        return stream
    else:
        result = original_method(*args, **kwargs)
        return result
    return None


def stream_next_wrapper(original_method, *args, **kwargs):
    print(f"Before calling {original_method.__name__}")
    result = original_method(*args, **kwargs)
    print(f"After calling {original_method.__name__}")
    print(result)
    return result


def stream_iter_wrapper(original_method, *args, **kwargs):
    print(f"Before calling {original_method.__name__}")
    result = original_method(*args, **kwargs)
    print(f"After calling {original_method.__name__}")
    print(result)
    return result


class OpenAIWrapper(_OpenAI):
    pass


def _wrapper_init(original_method, *args, **kwargs):
    """
    Example of a wrapper function that can be used with add_method_wrapper.

    Args:
        original_method: The original method to be wrapped.
        *args, **kwargs: Arguments and keyword arguments for the original method.

    Returns:
        The result of the original method call.
    """
    logger.info(f"Initializing {original_method.__name__}")
    result = original_method(*args, **kwargs)
    logger.info(f"Adding method wrappers {original_method.__name__}")
    self = args[0]
    wrap_method(self.chat.completions, "create", chat_wrapper)
    logger.info(f"After calling {original_method.__name__}")
    return result


wrap_method(OpenAIWrapper, "__init__", _wrapper_init)

# add_method_kwarg(OpenAIWrapper, "__init__", "speck_log", 69)
