import collections


class Reference():
    # Wraps object and associate it with priority.
    def __init__(self, _object) -> None:
        # _object: Any python object
        self._object = _object

    def set_object(self, _object):
        self._object = _object

    def get_object(self):
        return self._object

    def get_type(self):
        # returns type of underlying object
        return self._object.__class__

    @classmethod
    def to_reference(cls, _object):
        # Creates refence object from provided object.
        if isinstance(_object, Reference):
            _item = _object
        else:
            _item = cls(_object)
        return _item

    def is_callable(self):
        # Checks if underlying object is callable
        return callable(self._object)

    def is_iterable(self):
        # Checks if underlying object is iterable
        return isinstance(self._object, collections.Iterable)

    def is_iterator(self):
        # Checks if underlying object is iterator
        return isinstance(self._object, collections.Iterator)

    def is_string(self):
        # Checks if underlying object is string
        return isinstance(self._object, str)

    def is_bytes(self):
        # Checks if underlying object is bytes
        return isinstance(self._object, str)

    def is_string_bytes(self):
        # Checks if underlying object is string or bytes
        return self.is_string() or self.is_bytes()
