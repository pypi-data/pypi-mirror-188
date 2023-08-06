from typing import Any, Callable, Dict, Sequence, Tuple
from unittest.mock import MagicMock

import pytest
from magicgui import magicgui
from typing_extensions import Annotated

from napari_result_stack.types import StoredMeta


def test_store_result(stored: StoredMeta):
    @magicgui
    def f(x: int) -> stored[int]:
        return x

    assert list(stored.valuesof[int]) == []
    f(1)
    assert list(stored.valuesof[int]) == [1]
    f(2)
    assert list(stored.valuesof[int]) == [1, 2]


def test_receiving_stored_values(stored: StoredMeta):
    @magicgui
    def provide(x: int) -> stored[int]:
        return x

    @magicgui
    def receive(x: stored[int]):
        return x + 1

    assert list(stored.valuesof[int]) == []
    assert receive.x.choices == ()

    provide(1)
    assert list(stored.valuesof[int]) == [1]
    assert receive.x.choices == (1,)
    assert receive() == 2

    provide(2)
    assert list(stored.valuesof[int]) == [1, 2]
    assert receive.x.choices == (1, 2)


def test_independency(stored: StoredMeta):
    @magicgui
    def provide_0(x: int) -> stored[int, 0]:
        return x

    @magicgui
    def receive_0(x: stored[int, 0]):
        return x + 1

    @magicgui
    def provide_1(x: int) -> stored[int, 1]:
        return x

    @magicgui
    def receive_1(x: stored[int, 1]):
        return x + 1

    assert list(stored.valuesof[int, 0]) == []
    assert list(stored.valuesof[int, 1]) == []
    provide_0(-1)
    assert list(stored.valuesof[int, 0]) == [-1]
    assert list(stored.valuesof[int, 1]) == []
    provide_1(-2)
    assert list(stored.valuesof[int, 0]) == [-1]
    assert list(stored.valuesof[int, 1]) == [-2]

    assert receive_0.x.choices == (-1,)
    assert receive_1.x.choices == (-2,)


def test_list_like_methods(stored: StoredMeta):
    stored[str]
    stored.valuesof[str].append("a")
    stored.valuesof[str].append("b")
    stored.valuesof[str].append("c")
    stored.valuesof[str][0] == "a"
    stored.valuesof[str][1] == "b"
    stored.valuesof[str][2] == "c"
    assert list(stored.valuesof[str]) == ["a", "b", "c"]
    stored.valuesof[str].pop(1)
    assert list(stored.valuesof[str]) == ["a", "c"]
    stored.valuesof[str].clear()
    assert list(stored.valuesof[str]) == []


def test_get_method(stored: StoredMeta):
    stored[str]
    stored.valuesof[str].maxsize = 3
    for i in range(5):
        stored.valuesof[str].append(str(i))
    assert stored.valuesof[str][0] == stored.valuesof[str].get(2)
    assert stored.valuesof[str][1] == stored.valuesof[str].get(3)
    assert stored.valuesof[str][2] == stored.valuesof[str].get(4)
    assert 0 == stored.valuesof[str].get(5, 0)
    with pytest.raises(KeyError):
        stored.valuesof[str].get(5)
    with pytest.raises(TypeError):
        stored.valuesof[str].get("a")


def test_overflow(stored: StoredMeta):
    stored[str]
    stored.valuesof[str].maxsize = 3
    with pytest.raises(ValueError):
        stored.valuesof[str].maxsize = 0
    assert stored.valuesof[str].maxsize == 3
    stored.valuesof[str].append("a")
    stored.valuesof[str].append("b")
    stored.valuesof[str].append("c")
    assert list(stored.valuesof[str]) == ["a", "b", "c"]
    stored.valuesof[str].append("d")
    assert list(stored.valuesof[str]) == ["b", "c", "d"]
    stored.valuesof[str].append("e")
    assert list(stored.valuesof[str]) == ["c", "d", "e"]


def test_setting_overflow(stored: StoredMeta):
    stored[str]
    stored.valuesof[str].append("a")
    stored.valuesof[str].append("b")
    stored.valuesof[str].append("c")
    assert list(stored.valuesof[str]) == ["a", "b", "c"]
    stored.valuesof[str].maxsize = 1
    assert list(stored.valuesof[str]) == ["c"]
    stored.valuesof[str].append("b")
    assert list(stored.valuesof[str]) == ["b"]


def test_last(stored: StoredMeta):
    @magicgui
    def f(s: str) -> stored[str]:
        return s

    @magicgui
    def g(s: stored.Lastof[str]):
        pass

    with pytest.raises(IndexError):
        g.s.value
    f("a")
    assert g.s.value == "a"
    f("b")
    assert g.s.value == "b"


def test_repr(stored: StoredMeta):
    repr(stored[str])
    repr(stored.valuesof[str])
    repr(stored.widgetof[str])


def test_magicgui_construction(stored: StoredMeta):
    @magicgui
    def provide() -> stored[int]:
        return 0

    @magicgui
    def receive(x: stored[int]):
        return x + 1

    @magicgui
    def receive_last(x: stored.Lastof[int]):
        pass

    provide.show()
    receive.show()
    receive_last.show()
    provide()
    receive()
    receive_last()


@pytest.mark.parametrize(
    "tp",
    [
        complex,
        type,
        tuple,
        Tuple[int, str],
        Dict[str, Any],
        Callable,
        Callable[..., int],
        Callable[[int, str], int],
        Annotated[int, "metadata"],  # NOTE: metadata must be hashable
        Sequence[str],
    ],
)
def test_type_names(tp, stored: StoredMeta):
    @magicgui
    def f() -> stored[tp]:
        return 0

    f()
    str(stored[tp])
    repr(stored[tp])


def test_instantiate_error(stored: StoredMeta):
    with pytest.raises(TypeError):
        stored()
    with pytest.raises(TypeError):
        stored[int]()
    with pytest.raises(TypeError):
        stored.Lastof()
    with pytest.raises(TypeError):
        stored.Lastof[int]()
    with pytest.raises(TypeError):
        stored[int][int]
    with pytest.raises(TypeError):
        stored[int, 0, 0]
    with pytest.raises(TypeError):
        stored[0]


def test_return_callback_of_inner_type(stored: StoredMeta):
    class T:
        pass

    from magicgui import register_type

    mock = MagicMock()

    register_type(T, return_callback=mock)

    @magicgui
    def f() -> stored[T]:
        pass

    mock.assert_not_called()
    f()
    mock.assert_called()
