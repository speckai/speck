import functools
import inspect
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
    # if not isinstance(original_method, MethodType):
    #     raise TypeError(
    #         f"Attribute {method_name} of {class_instance.__class__.__name__} is not a method"
    #     )

    @functools.wraps(original_method)
    def wrapped_method(*args, **kwargs):
        return wrapper(original_method, *args, **kwargs)

    setattr(class_instance, method_name, wrapped_method)


def add_method_arg(class_instance, method_name, new_arg_name, new_arg_default=None):
    """
    Dynamically adds a new positional argument to a method of a class instance.

    Args:
        class_instance: The instance of the class whose method is to be modified.
        method_name (str): The name of the method to modify.
        new_arg_name (str): The name of the new argument to add.
        new_arg_default: The default value of the new argument (None if not specified).
    """
    if not hasattr(class_instance, method_name):
        raise AttributeError(
            f"Method {method_name} not found in {class_instance.__class__.__name__}"
        )

    method = getattr(class_instance, method_name)
    if not isinstance(method, MethodType):
        raise TypeError(
            f"Attribute {method_name} of {class_instance.__class__.__name__} is not a method"
        )

    original_signature = inspect.signature(method)

    # Create a new parameter and add it to the original method's signature
    new_parameter = inspect.Parameter(
        name=new_arg_name,
        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
        default=new_arg_default,
    )
    new_signature = original_signature.replace(
        parameters=[new_parameter, *original_signature.parameters.values()]
    )

    # Update the method's signature
    method.__signature__ = new_signature


def add_method_kwarg(
    class_instance, method_name, new_kwarg_name, new_kwarg_default=None
):
    """
    Dynamically adds a new keyword argument to a method of a class instance.

    Args:
        class_instance: The instance of the class whose method is to be modified.
        method_name (str): The name of the method to modify.
        new_kwarg_name (str): The name of the new keyword argument to add.
        new_kwarg_default: The default value of the new keyword argument.
    """
    if not hasattr(class_instance, method_name):
        raise AttributeError(
            f"Method {method_name} not found in {class_instance.__class__.__name__}"
        )

    method = getattr(class_instance, method_name)
    # if not isinstance(method, MethodType):
    #     raise TypeError(
    #         f"Attribute {method_name} of {class_instance.__class__.__name__} is not a method"
    #     )

    original_signature = inspect.signature(method)

    # Create a new keyword parameter and add it to the original method's signature
    new_parameter = inspect.Parameter(
        name=new_kwarg_name,
        kind=inspect.Parameter.KEYWORD_ONLY,
        default=new_kwarg_default,
    )
    new_signature = original_signature.replace(
        parameters=[*original_signature.parameters.values(), new_parameter]
    )

    # Update the method's signature
    method.__signature__ = new_signature
