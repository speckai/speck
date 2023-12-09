import logging

from openai import OpenAI as _OpenAI

from ..util._wrapper import wrap_method

logger = logging.getLogger(__name__)


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


class OpenAIWrapper(_OpenAI):
    speck_log: int = 69
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
    wrap_method(self.chat.completions, "create", wrapper)
    logger.info(f"After calling {original_method.__name__}")
    return result


wrap_method(OpenAIWrapper, "__init__", _wrapper_init)
# add_method_kwarg(OpenAIWrapper, "__init__", "speck_log", 69)
