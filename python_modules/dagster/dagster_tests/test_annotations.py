import sys
from abc import abstractmethod
from typing import NamedTuple, get_type_hints

import pytest
from dagster._annotations import (
    PUBLIC,
    PublicAttr,
    deprecated,
    experimental,
    is_deprecated,
    is_experimental,
    is_public,
    public,
)
from typing_extensions import Annotated


@pytest.mark.parametrize(
    "decorator,predicate",
    [(public, is_public), (experimental, is_experimental), (deprecated, is_deprecated)],
)
class TestAnnotations:
    def test_annotated_method(self, decorator, predicate):
        class Foo:
            @decorator
            def bar(self):
                pass

        assert predicate(Foo, "bar")

    def test_annotated_property(self, decorator, predicate):
        class Foo:
            @decorator
            @property
            def bar(self):
                pass

        assert predicate(Foo, "bar")

    def test_annotated_staticmethod(self, decorator, predicate):
        class Foo:
            @decorator
            @staticmethod
            def bar():
                pass

        assert predicate(Foo, "bar")

    def test_annotated_classmethod(self, decorator, predicate):
        class Foo:
            @decorator
            @classmethod
            def bar(cls):
                pass

        assert predicate(Foo, "bar")

    def test_annotated_abstractmethod(self, decorator, predicate):
        class Foo:
            @decorator
            @abstractmethod
            def bar(self):
                pass

        assert predicate(Foo, "bar")


def test_public_attr():
    class Foo(NamedTuple("_Foo", [("bar", PublicAttr[int])])):
        ...

    hints = (
        get_type_hints(Foo, include_extras=True)
        if sys.version_info >= (3, 9)
        else get_type_hints(Foo)
    )
    assert hints["bar"] == Annotated[int, PUBLIC]
