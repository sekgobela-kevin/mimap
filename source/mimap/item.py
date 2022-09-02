# Defines Item class which wraps reference object along with its metadata.
# Item class also implements Priority so that it instancescan be used in 
# place of reference object or vice-verse.
# Reference can be used without Item object as it has its own priority.
# Item gives oportunity to overide that priority and metadata support.

from mimap import reference


class Priority():
    # Simple class for setting priority.
    # Classes supporting priority should implement this class.
    def __init__(self, priority) -> None:
        # Calling method within initializer can cause problems.
        # Care should be taken when extending method called by __init__().
        self._setup_priority(priority)

    def _setup_priority(self, priority):
        # Setup priority priority to avoid it from being None.
        if priority != None:
            self._priority = priority
        else:
            # This is default priority when priority is None.
            self._priority = 1

    def get_priority(self):
        return self._priority

    def set_priority(self, priority):
        self._priority = priority



class Item(Priority):
    # Links reference object to metadata and priority.
    # Item has precidence over reference own priority.
    def __init__(self, _reference, priority=None, _type=object, 
    strict=False):
        # _reference: Reference object or python any object
        # priority: None or number representing represnting priority.
        # _type: Expected type for object.
        
        self._type = _type
        self._strict = strict
        self._type = _type
        # Shouldnt super().__init__() be first call of __init__()?
        # Thats because super().__init__() calls another method which
        # is overided by this class(begining of problems).
        super().__init__(priority) 
        # Calling method within initializer can cause problems.
        # This should be avoided as possible to avoid hard issues.
        # __init__() should be for initialising data not method calls.
        self._setup_reference(_reference)


    def _setup_priority(self, priority):
        # Setup priority for reference from object if 'priority' arg
        # is not provided.
        # This method is not meant to be overiden(take care)
        super()._setup_priority(priority)
        if priority == None:
            try:
                # object is probaly type of Priority
                self._priority = self._reference.get_priority()
            except AttributeError:
                # Default priority is already set by super class.
                # This method does not overide super class version.
                pass

    def _setup_reference(self, _reference):
        # Creates reference object when neccessay
        # This method is not meant to be overiden(take care)
        if self._strict and not isinstance(_reference, reference.Reference):
                err_msg = "Reference needs to be instance of '{}' not " +\
                    "'{}' when 'strict' is enabled"
                err_msg = err_msg.format(
                    reference.Reference.__name__,
                    _reference.__class__.__name__
                )
                raise TypeError(err_msg)
        else:
            self._reference = reference.Reference.to_reference(_reference)
            if not isinstance(_reference, self._type):
                err_msg = "object should be instance of {}, not {}"
                raise TypeError(err_msg.format(_reference, self._type))

    @classmethod
    def to_item(cls, _object):
        # Creates item object from if not already item object
        if isinstance(_object, Item):
            _item = _object
        else:
            _item = cls(_object)
        return _item

    def get_reference(self):
        # Returns underling reference object
        return self._reference

    def get_type(self):
        # Gets type of underlying reference
        return self._reference.get_type()

    def get_object(self):
        # Gets object of underlying reference
        return self._reference.get_object()

    def copy(self):
        # Returns copy of this object/instance
        return self.__class__(self._reference, self._priority, self._type, 
        self._strict)


if __name__ == "__main__":

    item = Item(10)
    print(item.get_priority())