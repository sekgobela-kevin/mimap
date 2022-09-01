# Defines classes for represensting collection of items.
# The items can be ranked and sorted based on their priorities.
# The classes also implement priority methods just as references and items.
# That allows the classes to be used for creating references and items.

from mimap import item
from mimap import reference


class Block(reference.Priority):
    # Wraps collection of Item objects and associate them with priority.
    def __init__(self, items, priority=None, strict=True) -> None:
        # items: Collection of Item objects
        # priority: Number representing priority for items.
        super().__init__(priority)
        self.__setup_items(items, strict)
        self.__setup_priority(priority)
        self._strict = strict

    def __setup_priority(self, priority):
        # Setup priority from average of items priorities.
        # Default priority is already set by super class.
        if priority == None:
            # Calculates priority from average of priorities of items.
            priorities = [_item.get_priority() for _item in self._items]
            average_priority = sum(priorities)/len(priorities)
            self._priority = average_priority

    def __setup_items(self, items, strict):
        # Setup items to ensure they are in correct type.
        # Item objects will be created when neccessary.
        # This could make find bugs hard but it simplifies things.
        new_items = []
        for _item in items:
            if isinstance(_item, item.Item):
                new_item = _item
            else:
                new_item = item.Item(_item)
                if strict:
                    _reference = new_item.get_reference()
                    _object = _reference.get_object()
                    if isinstance(_object, Block):
                        err_msg = "Nested Block objects not allowed " +\
                            "when 'strict' is enabled"
                        raise TypeError(err_msg)
            new_items.append(new_item)
        self._items = new_items

    def _rank_items(self, items):
        # Returns items sorted by their priority
        return sorted(items, key=lambda _item: _item.get_priority())

    def get_items(self, rank=True):
        # Returns items stored in block object.
        # When 'rank' is True items will be ranked else return unchanged.
        if rank:
            return self._rank_items(self._items)
        else:
            return self._items

    def get_references(self, rank=True):
        # Returns reference underlying item objects
        items = self.get_items(rank)
        return [item.get_reference() for item in items]

    def get_objects(self, rank=True):
        # Returns original underlying objects items references.
        references = self.get_references(rank)
        return [_reference.get_object() for _reference in references]

    def __iter__(self):
        return iter(self.get_items())

    def __len__(self):
        return len(self._items)


if __name__ == "__main__":

    item_object = item.Item(reference.Reference(object), {"priority": 40})
    item_object2 = item.Item(10, {"priority": 12})

    block_object = Block(
        [reference.Reference(10, 20), Block([200000])], strict=False)

    print(block_object.get_objects(True))
    print(len(block_object))