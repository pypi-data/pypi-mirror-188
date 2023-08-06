from typing import Any, Iterable

from pyhandling.shortcuts import *
from tests.mocks import Box

from pytest import mark


@mark.parametrize('result, object_, method_name', (('<Box instance>', Box(), '__repr__'), ))
def test_callmethod(result: Any, object_: object, method_name: str):
    assert callmethod(object_, method_name) == result


@mark.parametrize(
    'input_collections, output_collection',
    [
        [((1, 2, 3), (4, 5)), (1, 2, 3, 4, 5)],
        [((1, 2), tuple(), (3, 4, 5), tuple(), (6, 7)), (1, 2, 3, 4, 5, 6, 7)],
        [((1, 2, 3), (4, (5, 6))), (1, 2, 3, 4, (5, 6))],
        [[[[[[42]]]]], ([[[42]]], )],
        [tuple(), tuple()],
    ]
)
def test_summed_collection_from(input_collections: Iterable[Iterable], output_collection: tuple):
    assert summed_collection_from(*input_collections) == output_collection


@mark.parametrize(
    "first_node, second_node, input_resource",
    [(lambda x: x * 2, str, 16), (str, lambda x: x * 2, 1)]
)
def test_next_action_decorator_of(first_node: Callable, second_node: Callable[[Any], Any], input_resource: Any):
    assert (
        next_action_decorator_of(second_node)(first_node)(input_resource)
        == ActionChain(first_node, second_node)(input_resource)
    )


@mark.parametrize(
    "first_node, second_node, input_resource",
    [(lambda x: x * 2, str, 16), (str, lambda x: x * 2, 1)]
)
def test_previous_action_decorator_of(first_node: Callable, second_node: Callable[[Any], Any], input_resource: Any):
    assert (
        previous_action_decorator_of(first_node)(second_node)(input_resource)
        == ActionChain(first_node, second_node)(input_resource)
    )


@mark.parametrize(
    "func, arguments, extra_arguments",
    [(pow, (4, 2), tuple()), (pow, (4, 4), (1, 2, 3))]
)
def test_event_as(func: Callable, arguments: Iterable, extra_arguments: Iterable):
    assert event_as(func, *arguments)(extra_arguments) == func(*arguments)


@mark.parametrize("items", [(1, 2, 3), "Hello world!", range(10)])
def test_collection_from(items: Iterable):
    assert collection_from(*items) == tuple(items)


@mark.parametrize(
    "resource, arguments",
    [
        (256, tuple()),
        (42, (1, 2, 3)),
        (None, (1, 2, 3)),
    ]
)
def test_take(resource: Any, arguments: Iterable):
    assert take(resource)(*arguments) == resource