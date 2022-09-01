# Defines classes related to reference.
# Reference class wraps any object along with its priority.
# It also contain methods for knowing more about underlying object.
# Priority of reference helps in ranking the reference.

import collections


class Priority():
    # Simple class for setting priority.
    # Classes supporting priority should implement this class.
    def __init__(self, priority) -> None:
        self.__setup_priority(priority)

    def __setup_priority(self, priority):
        # Setup priority priority to avoid it from being None.
        if priority != None:
            self._priority = priority
        else:
            # This is default priority when priority is None.
            self._priority = 1

    def get_priority(self):
        # Returns priority for reference if set else returns 1
        return self._priority 


class Reference(Priority):
    # Wraps object and associate it with priority.
    def __init__(self, _object, priority=None, _type=object) -> None:
        # _object: Any python object
        # priority: None or number representing represnting priority.
        # _type: Expected type for object.
        super().__init__(priority)
        if not isinstance(_object, _type):
            err_msg = "object should be instance of {}, not {}"
            raise TypeError(err_msg.format(_object, _type))
        self._object = _object
        self.__setup_priority(priority)

    def __setup_priority(self, priority):
        # Setup priority for reference from object if 'priority' arg
        # is not provided.
        if priority == None:
            try:
                # object is probaly type of Priority
                self._priority = self._object.get_priority()
            except AttributeError:
                # Default priority is already set by super class.
                # This method does not overide super class version.
                pass

    def get_object(self):
        # returns undelyimng object
        return self._object

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
