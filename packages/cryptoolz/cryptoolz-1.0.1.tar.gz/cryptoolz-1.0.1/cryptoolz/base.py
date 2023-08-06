import abc

from typing import Any, List, Callable, Optional

from pydantic import BaseModel


class Super:
    @staticmethod
    def PreCall(func):
        def PrecallsSuper(self, *args, **kwargs):
            getattr(super(type(self), self), func.__name__)(*args, **kwargs)
            return func(self, *args, **kwargs)

        return PrecallsSuper


class AdHoc:
    @staticmethod
    def ListMorph(index) -> Callable[..., Any]:
        def Decorator(func) -> Callable[..., Any]:
            def Morphed(self, *args, **kwargs) -> Any:
                results: List[Any] = []
                if isinstance(args[index], list):
                    for val in args[index]:
                        results.append(
                            func(
                                self, *args[0:index], val, *args[index + 1 :], **kwargs
                            )
                        )
                    return results
                else:
                    return func(self, *args, **kwargs)

            return Morphed

        return Decorator


class Checkpointed:
    _call_order_predicate: Callable[[int, int], bool]

    index: int

    def EnforceCallOrder(checkpoint_name):
        def Decorator(func):
            def Wrapper(self, *args, **kwargs):
                checkpoint = getattr(self, checkpoint_name)

                if not self._call_order_predicate(checkpoint._index, self.index):
                    raise RuntimeError(
                        f"{self}: call order of functions must satisfy predicate {self._call_order_predicate.__name__}!"
                    )

                result = func(self, *args, **kwargs)

                self.advance_to_checkpoint(checkpoint._index)

                return result

            return Wrapper

        return Decorator

    def __init__(self, predicate: Callable[[int, int], bool]):
        self.index = 0
        self._call_order_predicate = predicate

    def advance_to_checkpoint(self, checkpoint: int) -> None:
        self.index = checkpoint


class Checkpoint(abc.ABC):
    _index: int

    def __assert_other_checkpoint(other):
        if not isinstance(other, Self):
            raise TypeError(
                "Checkpoint: instance being compared with is not a Checkpoint!"
            )

    def __init__(self, index: int):
        self._index = index

    def __call__(self, *args, **kwargs):
        return self._logic(*args, **kwargs)

    @abc.abstractmethod
    def _logic(self, *args, **kwargs) -> Any:
        pass

    def __lt__(self, other):
        self.__assert_other_checkpoint(other)
        return self._index < other._index

    def __le__(self, other):
        self.__assert_other_checkpoint(other)
        return self._index <= other._index

    def __eq___(self, other):
        self.__assert_other_checkpoint(other)
        return self._index == other._index

    def __ne___(self, other):
        self.__assert_other_checkpoint(other)
        return self._index != other._index

    def __gt___(self, other):
        self.__assert_other_checkpoint(other)
        return other._index < self._index

    def __ge___(self, other):
        self.__assert_other_checkpoint(other)
        return other._index <= self._index
