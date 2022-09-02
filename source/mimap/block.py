# Defines classes for represensting collection of items.
# The items can be priority_sorted and sorted based on their priorities.
# The classes also implement priority methods just as references and items.
# That allows the classes to be used for creating references and items.

from mimap import item

from collections import defaultdict
import numbers


class Block(item.Priority):
    # Wraps collection of Item objects and associate them with priority.
    def __init__(self, items, priority=None, _type=object, strict=True,
    priority_mode=None):
        # items: Collection of Item objects
        # priority: Number representing priority for items.
        self._items = items
        self._strict = strict
        self._type = _type
        self._strict = strict
        # Calling methods with initializer causes problems.
        # Thats why super().__init__() is fist call to __init__().
        self._setup_priority_mode(priority_mode)
        # super().__init__() setup priority.
        # priority_mode need to be setup before setting priority.
        # This will cause problems when methods are overiden.
        super().__init__(priority)
        # Setup items after priority have been set from existing items.
        self._setup_items(items)
        # Calling method within initializer is hell.
        # The instance is not yet fully created.
        # Warning has been included on the methods called by __init__().

    def _setup_priority(self, priority):
        # Setup priority from average of items priorities.
        # Default priority is already set by super class.
        # This method is not meant to be overiden(take care)
        if priority == None:
            # Priority was suppossed to be calculated from average.
            # But priority can be non number(that makes it impossible).
            # Median is used here to calculate priority for block.
            # That allows non numbers to be used as priority without error.
            priorities = [_item.get_priority() for _item in self._items]
            # Empty priorities wont work(rather be default one)
            if priorities:
                if self._priority_mode == "median":
                    # Calculates priority from median(midpoint).
                    # This is based on position other than values.
                    # It will work even if priorities are non numbers.
                    priorities.sort(reverse=True)
                    # Find midpoint index of priorities list
                    median_index = round((len(priorities)-1)/2)
                    # Use the index to find meadin priority.
                    _priority = priorities[median_index]
                elif self._priority_mode in {"average", "avg", "mean"}:
                    # Calculates avarage of priorities.
                    # Priorities needs to be numbers to work.
                    _priority = sum(priorities)/len(priorities)
                elif self._priority_mode == "min":
                    # Minumum of priorities is used as block priority.
                    _priority = min(priorities)
                elif self._priority_mode == "max":
                    # Maximum of priorities is used as block priority.
                    _priority = max(priorities)
                else:
                    err_msg = "priority_mode should one of {} not '{}'"
                    priority_modes = ("min", "max","median", "average", 
                    "avg", "mean")
                    err_msg = err_msg.format(priority_modes, 
                    self._priority_mode)
                    raise ValueError(err_msg)
                self._priority = _priority
        else:
            self._priority = priority

    def _to_items(self, _items_like):
        # Returns item object from iterator of objects.
        # Item objects will be returned unchanged.
        # Non item objects will be result in item objects.
        return  [item.Item.to_item(_item) for _item in self.get_items()]

    def _setup_items(self, items):
        # Setup items to ensure they are in correct type.
        # Item objects will be created when neccessary.
        # This could make find bugs hard but it simplifies things.
        # This method is not meant to be overiden(take care)
        new_items = []
        for _item in items:
            new_item = item.Item.to_item(_item)
            # Gets underlying object of item object
            _reference = new_item.get_reference()
            _object = _reference.get_object()
            # Check if strict is respected(Block objects not allowed).
            # Exception is raised if not respected.
            if self._strict and isinstance(_object, Block):
                err_msg = "Nested Block objects not allowed when " +\
                    "'strict' is enabled"
                raise TypeError(err_msg)
            # Check if type for object is correct.
            # Exception is if type of object does not match expected one.
            if not isinstance(_object, self._type):
                err_msg = "Item should have reference of type '{}' not '{}'"
                type_name = _object.__class__.__name__
                err_msg = err_msg.format(self._type.__name__, type_name)
                raise TypeError(err_msg)
            # Appends new item to items list
            new_items.append(new_item)
        self._items = self._get_items_with_new_priorities(new_items)

    def _setup_priority_mode(self, priority_mode):
        # This method is not meant to be overiden(take care)
        if priority_mode == None:
            self._priority_mode = "median"
        else:
            self._priority_mode = priority_mode

    def _priority_sort_items(self, items):
        # Returns items sorted by their priority
        return sorted(items, key=lambda _item: _item.get_priority())

    def _get_items_with_new_priorities(self, items):
        # Returns copy of items with updated priorities.
        new_items = []
        for _item in items:
            # Copies item object(avoid modifying original object)
            new_item = _item.copy()
            if isinstance(self._priority, numbers.Number):
                # Also modifies priority of copied item.
                # New priority is between item priority and block priority.
                # Average is the best as it satisfies both block and item 
                # priority equally.
                new_priority = (self._priority + new_item.get_priority())/2
                new_item.set_priority(new_priority)
            new_items.append(new_item)
        return new_items

    def set_priority(self, priority):
        # Sets priority for block and update items priorities
        super().set_priority(priority)
        self._items = self._get_items_with_new_priorities(self._items)     


    def get_items(self, priority_sort=True):
        # Returns items stored in block object.
        # When 'priority_sort' is True items will be sorted by priorities.
        if priority_sort:
            return self._priority_sort_items(self._items)
        else:
            return self._items

    def get_priorities(self):
        # Gets priorities of block item objects
        return [_item.get_priority() for _item in self.get_items()]

    def get_references(self, priority_sort=True):
        # Returns reference underlying item objects
        items = self.get_items(priority_sort)
        return [item.get_reference() for item in items]

    def get_objects(self, priority_sort=True):
        # Returns original underlying objects items references.
        references = self.get_references(priority_sort)
        return [_reference.get_object() for _reference in references]

    def to_tuple(self):
        # Returns tuple form of block with priorities and objects.
        # Priority will be used as tuple key and object as value.
        # object is the object under reference object of item.
        _items = self.get_items()
        results = []
        for _item in _items:
            results.append((_item.get_priority(), _item.get_object()))
        return tuple(results)

    def to_dict(self):
        # Returns dict form of block with priorities and objects.
        # This will fail if priority not hashable.
        return dict(self.to_tuple())

    def to_multi_dict(self):
        result_dict = defaultdict(set)
        for _priority, _object in self.to_tuple():
            result_dict[_priority].add(_object)
        return result_dict
    
    def __iter__(self):
        for _priority, _object in self.get_items():
            yield _priority, _object

    def __len__(self):
        return len(self._items)


class DeepBlock(Block):
    # Block that allows retrieving of deep items
    def __init__(self, items, priority=None, _type=object, strict=False,
    priority_mode=None):
        super().__init__(items, priority, _type, strict)
    
    def _extract_deep_items(cls, _block):
        # Extracts low level(deep) items from block object.
        # This include item objects not containing block object.
        # This method is called by _setup_items().
        # Take care when extensing it on sub classes.
        deep_items = []
        # Gets item objects of block(not sorted by priority)
        items = _block.get_items(False)
        for _item in items:
            # Gets reference from item
            _reference = _item.get_reference() 
            # Gets object from reference
            _object = _reference.get_object() 
            # Checks if object of reference is block object.
            # Uses recursion if the object is block object.
            # Recursion continues until non block item is found.
            if isinstance(_object, Block):
                # Extract non block items from the block object.
                block_deep_items = cls._extract_deep_items(_object)
                deep_items.extend(block_deep_items)
            else:
                # This item does not contain block object
                deep_items.append(_item)
        return deep_items

    def _setup_items(self, items):
        # Setup deep items overiding existing item objects.
        # Ensures all items are really item objects.
        # _extract_deep_items() expectes item objects.
        self._items = self._to_items(self.get_items())
        _items = self._extract_deep_items(self)
        # Now asks super class to setup items as usual.
        # Items priorities will be updated as expected.
        super()._setup_items(_items)


if __name__ == "__main__":
    from mimap import reference

    item_object = item.Item(reference.Reference("Ruth"))
    item_object2 = item.Item("Marry")
    item_object3 = item.Item("John", 400)

    items = [item_object, item_object2, item_object3]

    block_object = Block(items)
    deep_object = DeepBlock([Block(items), Block([item.Item("Lord")])], 30, priority_mode="avg")

    print(block_object.to_tuple())
    print(deep_object.to_tuple())