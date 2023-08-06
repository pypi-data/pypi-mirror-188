"""
Copyright 2022 nMachine.io

Provides the decorator @classproperty.
"""


class ClassPropertyDescriptor:
    """Implements getter/setter for class property"""

    def __init__(self, fget, fset=None):  # type: ignore
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):  # type: ignore
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):  # type: ignore
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):  # type: ignore
        """Setter for properties"""
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):  # type: ignore
    """Decorator for class properties"""
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)
