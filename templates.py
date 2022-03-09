from typing import Callable, TypeVar, Generic, NoReturn
from typing_extensions import ParamSpec, Concatenate
from inspect import signature

__all__ = (
  "TemplateError",
  "template",
  "_GenericedTemplate",
  "Template"
)

T = TypeVar("T")

P = ParamSpec("P")
F = ParamSpec("F")

class TemplateError(Exception):
    """Raised when an invalid number of generics is passed."""
    pass

class _GenericedTemplate(Generic[P, T]):
    """Class representing a function with passed in generics."""
    
    def __init__(self, caller: Callable[P, T], *generics: str) -> None:
        self._generics = generics
        self._caller = caller

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self._caller(*args, **kwargs)

class Template(Generic[P, T, F]):
    """Class representing a templated function."""
    
    def __init__(self, caller: Callable[F, Callable[P, T]]):
        self._generics = len(signature(caller).parameters)
        self._callable = caller

    def __call__(self, *_, **__) -> NoReturn:
        raise ValueError(f"function {self._callable.__name__} requires generics")
    
    def __getitem__(self, a: F.args, **_: F.kwargs) -> _GenericedTemplate[P, T]: # type: ignore
        args = [a] if not isinstance(a, tuple) else a

        if len(args) != self._generics:
            raise TemplateError(
                f"function {self._callable.__name__} requires exactly {self._generics} generics, got {len(args)}"
            )

        return _GenericedTemplate(self._callable(*args), *args)

def template(func: Callable[F, Callable[P, T]]) -> Template[P, T, F]:
    """Make a function a template."""
    return Template(func)