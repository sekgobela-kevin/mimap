from mimap import reference
import inspect


class Value(reference.Reference):
    '''Defines value to be used with item'''
    # Used for error messages
    _name = "value"
    # Default value when value is not provided.
    _default_value = ...

    def __init__(self, value) -> None:
        super().__init__(value)

    @classmethod
    def get_name(cls):
        return cls.name

    @classmethod
    def get_default_value(cls):
        return cls._default_value

    def is_method_func(self):
        # Checks if object if value is function or method.
        if self.is_callable():
            if inspect.isfunction(self._object):
                return True
            else:
                return inspect.ismethod(self._object)
        return False

    def get_value(self, *args, **kwargs):
        # Gets value behind this object.
        # Object of method or function will result in return value
        # of that callable.
        if self.is_method_func():
            return self._object(*args, **kwargs)
        elif isinstance(self._object, Value):
            return self._object.get_value()
        else:
            return self._object

    def set_value(self, value):
        self._object = value


class Priority(Value):
    # Simple class for setting priority.
    # Classes supporting priority should implement this class.
    _name = "priority"
    _default_value = None

    def __init__(self, priority) -> None:
        super().__init__(priority)

    def get_priority(self, *args, **kwargs):
        # Gets priority value
        return self.get_value(*args, **kwargs)

    def set_priority(self, priority):
        # Sets priority value
        self.set_value(priority)


