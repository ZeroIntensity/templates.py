# templates.py

## Simple function templating for Python.

### Example

```py
from templates import template
from typing import Type

@template
def cast(t: Type):
    def inner(val: str):
        return t(val)

    return inner

casted = cast[tuple]("abc")
print(casted) # ("a", "b", "c")
```

### Installation

#### Linux/macOS

```
python3 -m pip install -U templates.py
```

#### Windows

```
py -3 -m pip install -U templates.py
```

### Usage

Start with decorating a function with `templates.template` and putting the generics in your signature, like so:

```py
from templates import template

@template
def my_template(a: str, b: str, c: str): # needs to get called using my_template[a, b, c]()
    ...
```

Now, for the actual functionality, you need to define another function inside it.

Make sure to return the inner function!

Example:

```py
from templates import template

@template
def my_template(a: str, b: str, c: str):
    def inner(test: str):
        ...
    return inner # you always need to return the inner function
```

### Limitations

#### Type Checking Issue

Due to `typing_extensions.ParamSpec` being horrible, the following code will not raise an type issue (at least when using pylance)

```py
@template
def add(a: int, b: int):
    def inner(c: int) -> int:
        return a + b + c
    return inner

a = test[1, 2, 3](4) # only raises a runtime error
print(a)
```

Luckily, you can still see the needed generics when hovering over the template call.

#### Default Generics

Default generics are not supported:

```py
@template
def my_template(a: str, b: str, c: str = "c"):
    def inner(test: str):
        ...
    return inner

my_template["a", "b"]("hi") # raises templates.TemplateError
```

#### Return Type Annotation

There is no good way to annotate function return type:

```py
@template
def my_template(a: str, b: str, c: str) -> str: # typing error!
    def inner(test: str):
        ...
    return inner

my_template["a", "b", "c"]("hi")
```

However, you **can** set the return type of the inner function:

```py
@template
def my_template(a: str, b: str, c: str):
    def inner(test: str) -> str: # do this instead!!
        ...
    return inner

my_template["a", "b", "c"]("hi")
```
