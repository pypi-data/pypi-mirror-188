# Noldor

Noldor is a Python validation library easy to extend.

It is easily compatible with [dataclasses](https://docs.python.org/3/library/dataclasses.html), [attrs](https://github.com/python-attrs/attrs) and [pydantic](https://github.com/pydantic/pydantic).

## Installation

```
pip install noldor
```

## Usage with classes

Assume you have the following class defined:

```python
class Person:
    
    name: str
    age: int
```

You want to be sure that the name string is longer than zero characters and also that the age is an integer value greater than 0.

### Dataclass

```python
from dataclasses import dataclass
from noldor import validate
from noldor.validators import longer_than, greater_than

@dataclass
class Person:
    
    name: str
    age: int

    def __post_init__(self) -> None:
        validate(self.name, longer_than(0))
        validate(self.age, greater_than(0))
```

### Attrs
```python
from attrs import define
from noldor import validate
from noldor.validators import longer_than, greater_than

@define
class Person:
    
    name: str
    age: int

    def __attrs_post_init__(self) -> None:
        validate(self.name, longer_than(0))
        validate(self.age, greater_than(0))
```


### Pydantic

```python
from pydantic.dataclasses import dataclass
from noldor import validate
from noldor.validators import longer_than, greater_than

@dataclass
class Person:

    name: str
    age: int

    def __post_init__(self) -> None:
        validate(self.name, longer_than(0))
        validate(self.age, greater_than(0))
```

In any case, if you create a Person object that does not respect the given constraints, a ValueError is raised. The ValueError contains the log of the validation process as the first argument.

```python
>>> p = Person(name="Max", age=-1)

...

ValueError: [red]NOT RESPECTED[/red]: -1 must be greater than 0
```

### Multiple constraints for one value

Notice that you can specify multiple constraints on a given value. For example, if you want the name of a Person to be also shorter than 30 characters (example given only with dataclasses for simplicity):

```python
from dataclasses import dataclass
from noldor import validate
from noldor.validators import longer_than, shorter_than, greater_than

@dataclass
class Person:
    
    name: str
    age: int

    def __post_init__(self) -> None:
        validate(self.name, longer_than(0), shorter_than(30))
        validate(self.age, greater_than(0))
```

## General usage
Noldor is probably perfectly compatible with other libraries and its usage is not restricted to the validation of class attributes. In fact, Noldor can be exploited for validating any kind of value.

For example, imagine you got an integer value from the user input. You want to check that the value is a positive prime integer. You can do this way:

```python
from noldor import validate
from noldor.validators import is_positive, is_prime

if __name__ == "__main__":
    N = int(input())
    validate(N, is_positive(), is_prime())
```

If you do not want to throw a ValueError when a constraint is not satisfied, you can use the `check` function. This function returns a `Response` object, containing a boolean value that represents the result of the validation (True if all conditions are satisfied, False if at least one condition is not satisfied):

```python
from noldor import check
from noldor.validators import is_positive, is_prime

if __name__ == "__main__":
    N = int(input())
    res = check(N, is_positive(), is_prime())
    if res.result is True:
        print(f"{N} is a valid value!", res.log)
    else:
        print(f"{N} is **not** a valid value.", res.log)
```

## Create your custom validator

We call "validator" a function returning a Validator object.
A Validator object contains:
- a *condition*: a function that returns a boolean value;
- a *name*: a name for the validator, exploited to write the log of the validation.

Here follows the definition of the validator `multiple_of`:

```python
def longer_than(lower_bound: int) -> Validator[Sized]:
    return Validator[Sized](
        lambda x: len(x) > lower_bound,
        f"longer than {lower_bound}"
    )
```

You can find a lot of examples of validators in the folder `noldor/validators`.

Noldor is a tiny library, easy to expand. If you write a validator that can be useful to many others, feel free to issue a pull request!