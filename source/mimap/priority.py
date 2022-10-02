import pemap


class Priority(pemap.Value):
    # Value class for representing priority
    _default_value = None
    _value_attr_names = ("priority", "get_priority")

    def get_priority(self, *args, **kwargs):
        # Gets priority value
        return self.get_value(*args, **kwargs)

    def set_priority(self, priority):
        # Sets priority value
        self.set_value(priority)
