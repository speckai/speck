import functools
import logging
from types import MethodType

logger = logging.getLogger(__name__)


def wrap_method(class_instance, method_name, wrapper):
    """
    Applies a wrapper function to a method of a class instance.

    Args:
        class_instance: The instance of the class whose method is to be wrapped.
        method_name (str): The name of the method to wrap.
        wrapper (function): The wrapper function to apply.

    Raises:
        AttributeError: If the specified method does not exist in the class instance.
        TypeError: If the specified attribute is not a method.
    """
    if not hasattr(class_instance, method_name):
        raise AttributeError(
            f"Method {method_name} not found in {class_instance.__class__.__name__}"
        )

    original_method = getattr(class_instance, method_name)
    if not isinstance(original_method, MethodType):
        raise TypeError(
            f"Attribute {method_name} of {class_instance.__class__.__name__} is not a method"
        )

    @functools.wraps(original_method)
    def wrapped_method(*args, **kwargs):
        return wrapper(original_method, *args, **kwargs)

    setattr(class_instance, method_name, wrapped_method)
