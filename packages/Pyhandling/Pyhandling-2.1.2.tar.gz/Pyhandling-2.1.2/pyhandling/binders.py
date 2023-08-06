from functools import wraps, partial
from typing import Callable, Any, Iterable

from pyannotating import method_of

from pyhandling.annotations import handler_of
from pyhandling.tools import ArgumentPack


def bind(func: Callable, argument_name: str, argument_value: Any) -> Callable:
    """
    Atomic partial function for a single keyword argument whose name and value
    are separate input arguments.
    """

    return wraps(func)(partial(func, **{argument_name: argument_value}))


def post_partial(func: Callable, *args, **kwargs) -> Callable:
    """
    Function equivalent to functools.partial but with the difference that
    additional arguments are added not before the incoming ones from the final
    call, but after.
    """

    @wraps(func)
    def wrapper(*wrapper_args, **wrapper_kwargs) -> Any:
        return func(*wrapper_args, *args, **wrapper_kwargs, **kwargs)

    return wrapper


def mirror_partial(func: Callable, *args, **kwargs) -> Callable:
    """
    Function equivalent to pyhandling.handlers.rigth_partial but with the
    difference that additional arguments from this function call are unfolded.
    """

    return post_partial(func, *args[::-1], **kwargs)


def close(resource: Any, *, closer: method_of[Any] = partial) -> Callable:
    """
    Function to create a closure for the input resource.

    Wraps the input resource in a container function that can be \"opened\" when
    that function is called.

    The input resource type depends on the chosen closer function.

    With a default closer function, ***it requires a Callable resource***.

    When \"opened\" the default container function returns an input resource with
    the bined input arguments from the function container.
    """

    return partial(closer, resource)


def unpackly(func: Callable) -> handler_of[ArgumentPack]:
    """
    Decorator function that allows to bring an ordinary function to the handler
    interface by unpacking the input argument pack into the input function.
    """

    return wraps(func)(lambda pack: pack.call(func))