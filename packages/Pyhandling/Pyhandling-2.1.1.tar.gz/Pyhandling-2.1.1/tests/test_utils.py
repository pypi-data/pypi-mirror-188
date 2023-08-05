from functools import partial
from typing import Any, Type, Iterable, Callable

from pytest import mark, raises

from pyhandling.branchers import ActionChain, eventually
from pyhandling.errors import BadResourceError
from pyhandling.synonyms import raise_
from pyhandling.tools import ArgumentPack, BadResourceWrapper, IBadResourceKeeper
from pyhandling.utils import Logger, showly, documenting_by, calling_of, as_collection, times, raising, returnly_rollbackable, maybe, returnly_rollbackable, optionally_get_bad_resource_from
from tests.mocks import Counter, MockHandler, MockObject


@mark.parametrize(
    'initial_log_number, logging_amount',
    [(0, 0), (4, 0), (4, 8), (0, 8), (32, 16), (128, 128)]
)
def test_number_of_logger_logs(initial_log_number: int, logging_amount: int):
    logger = Logger((str(), ) * initial_log_number)

    for _ in range(logging_amount):
        logger(str())

    assert len(logger.logs) == initial_log_number + logging_amount


@mark.parametrize(
    "number_of_handlers, number_of_writer_calls",
    (
        ((0, 2), )
        + tuple(map(lambda x: (x, x + 1), range(1, 4)))
        + ((31, 32), (63, 64), (127, 128), (515, 516))
    )
)
def test_showly_by_logger(number_of_handlers: int, number_of_writer_calls: int):
    writing_counter = Counter()

    showly(
        (
            MockHandler()
            if number_of_handlers == 1
            else ActionChain((MockHandler(), ) * number_of_handlers)
        ),
        writer=lambda _: writing_counter()
    )(None)

    assert writing_counter.counted == number_of_writer_calls


@mark.parametrize(
    "documentation",
    (
        "Is a handler.", "Is a checker.", "Something.", str(),
        "\n\tIs something.\n\tOr not?", "\tIs a handler.\n\tIs a handler",
    )
)
def test_documenting_by(documentation: str):
    mock = MockObject()

    documenting_by(documentation)(mock)

    assert '__doc__' in mock.__dict__.keys()
    assert mock.__doc__ == documentation


@mark.parametrize(
    "object_, args, kwargs, result",
    [
        (lambda x, y: x * y + x + y, (2, 3), dict(), 11),
        (lambda x, y: x / y, (84,), dict(y=2), 42),
        (lambda: 256, tuple(), dict(), 256)
    ]
)
def test_calling_of(object_: Callable, args: Iterable, kwargs: dict, result: Any):
    assert calling_of(object_)(*args, **kwargs) == result


@mark.parametrize(
    "input_resource, result",
    [
        (42, (42, )),
        (None, (None, )),
        ([1, 2, 3], (1, 2, 3)),
        (map(lambda x: x ** 2, [4, 8, 16]), (16, 64, 256)),
        ((3, 9, 12), (3, 9, 12)),
        (tuple(), tuple()),
        (list(), tuple()),
        ('Hello', ('H', 'e', 'l', 'l', 'o'))
    ]
)
def test_as_collection(input_resource: Any, result: tuple):
    assert as_collection(input_resource) == result


@mark.parametrize(
    "steps_to_false, number_of_runs",
    [(3, 12), (0, 10), (1, 4), (10, 33)]
)
def test_times(steps_to_false: int, number_of_runs: int):
    runner = times(steps_to_false)

    inital_steps_to_false = steps_to_false

    for _ in range(inital_steps_to_false):
        assert runner() is (steps_to_false > 0)

        if steps_to_false <= 0:
            steps_to_false = inital_steps_to_false

        steps_to_false -= 1


@mark.parametrize(
    "error_type, error",
    [
        (TypeError, TypeError()),
        (IndexError, IndexError()),
        (KeyError, KeyError()),
        (Exception, Exception()),
        (Exception, KeyError())
    ]
)
def test_error_raising_of_raising(error_type: Type[Exception], error: Exception):
    with raises(error_type):
        raising(error_type)(error)


@mark.parametrize(
    "error_type, input_resource",
    [
        (Exception, str()),
        (TypeError, int()),
        (AttributeError, (1, 2, 3)),
        (AttributeError, (item for item in range(10))),
    ]
)
def test_resource_returning_of_raising(
    error_type: Type[Exception],
    input_resource: Any
):
    assert raising(error_type)(input_resource) == input_resource


@mark.parametrize(
    "handler, error_checker, input_resource, result",
    [
        (lambda x: x + 10, lambda _: True, 32, 42),
        (
            lambda x: x / 0,
            lambda error: isinstance(error, ZeroDivisionError),
            256,
            BadResourceError(256, ZeroDivisionError())
        ),
        (
            lambda x: x.non_existent_attribute,
            lambda error: isinstance(error, AttributeError),
            str(),
            BadResourceError(str(), AttributeError())
        ),
    ]
)
def test_returnly_rollbackable(
    handler: Callable[[Any], Any],
    error_checker: Callable[[Exception], Any],
    input_resource: Any,
    result: Any
):
    returnly_rollbackable_result = returnly_rollbackable(handler, error_checker)(input_resource)

    if type(result) is BadResourceError:
        assert returnly_rollbackable_result.bad_resource == result.bad_resource
        assert type(returnly_rollbackable_result.error) is type(result.error)

    else:
        assert returnly_rollbackable_result == result


@mark.parametrize(
    "handler, error_checker, input_resource, expected_error_type",
    [
        (lambda x: x / 0, lambda error: isinstance(error, TypeError), 32, ZeroDivisionError),
        (lambda x: 21 + x, lambda error: isinstance(error, AttributeError), '21', TypeError),
        (lambda x: x.non_existent_attribute, lambda error: isinstance(error, SyntaxError), tuple(), AttributeError),
    ]
)
def test_returnly_rollbackable_error_returning(
    handler: Callable[[Any], Any],
    error_checker: Callable[[Exception], Any],
    input_resource: Any,
    expected_error_type: Type[Exception]
):
    with raises(expected_error_type):
        returnly_rollbackable(handler, error_checker)(input_resource)


@mark.parametrize(
    "handler_resource, input_resource, result",
    [
        (ActionChain(lambda x: x + 2, BadResourceWrapper, lambda x: x.resource * 2), 40, 42),
        (returnly_rollbackable(lambda x: x / 0, lambda error: isinstance(error, ZeroDivisionError)), 42, 42),
        (ActionChain(), 42, ArgumentPack((42, ))),
        (tuple(), 256, ArgumentPack((256, ))),
        (lambda x: x ** x, 4, 256),
        ([lambda x: x ** 2, lambda x: x ** x], 2, 256),
        (
            [
                lambda x: x ** 2,
                lambda x: x ** x,
                lambda x: x + 80,
                lambda x: x >> 3,
                BadResourceWrapper
            ],
            2,
            42
        )
    ]
)
def test_maybe(
    handler_resource: Iterable[Callable] | Callable,
    input_resource: Any,
    result: Any
):
    maybe_result = maybe(handler_resource)(input_resource)

    assert (
        (maybe_result.bad_resource if isinstance(maybe_result, IBadResourceKeeper) else maybe_result)
        == result
    )


@mark.parametrize(
    "input_resource, result",
    [
        (42, 42),
        ((item for item in range(64)), ) * 2,
        (BadResourceWrapper("Some bad resource"), "Some bad resource"),
        (BadResourceError(256, Exception()), 256)
    ]
)
def test_optionally_get_bad_resource_from(input_resource: Any, result: Any):
    assert optionally_get_bad_resource_from(input_resource) == result