# Defines classes for represensting collection of items.
# The items can be priority_sorted and sorted based on their priorities.
# The classes also implement priority methods just as references and items.
# That allows the classes to be used for creating references and items.

from mimap import item

from collections import defaultdict
from queue import PriorityQueue
from numbers import Number


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
        # Returns item objects from iterator of objects.
        # Item objects will be returned unchanged.
        # Non item objects will  result in item objects.
        return  [item.Item.to_item(_item) for _item in _items_like]

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

    def _get_items_with_new_priorities(self, items):
        # Returns copy of items with updated priorities.
        new_items = []
        for _item in items:
            # Copies item object(avoid modifying original object)
            new_item = _item.copy()
            if isinstance(self._priority, Number):
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


    def get_items(self):
        # Returns items stored in block object.
        # When 'priority_sort' is True items will be sorted by priorities.
        return self._items

    def get_objects(self, priority_sort=True):
        # Returns original underlying objects from items
        return self.extract_objects_from_items(self._items)

    def get_priorities(self):
        # Gets priorities of block item objects
        return [_item.get_priority() for _item in self._items]

    @classmethod
    def extract_objects_from_items(cls, items):
        # Gets underlying object from item object
        return [_item.get_object() for _item in items]

    @classmethod
    def sort_items_by_priority(cls, items):
        # Returns items sorted by their priorities
        return sorted(items, key=lambda _item: _item.get_priority())

    def filter_items(self, key=None, limit=None):
        # Filters item objects filtered by key function
        filtered_items = list(filter(key, self._items))
        if limit != None:
            filtered_items = filtered_items[:limit]
        return filtered_items

    def find_items_by_priority(self, priority):
        # Finds item objects matching priority.
        def func(_item):
            return _item.get_priority() == priority
        return self.filter_items(func)

    def find_items_by_priorities(self, priorities):
        # Finds item objects matching any of priorities.
        def func(_item):
            return _item.get_priority() in priorities
        return self.filter_items(func)

    def find_items_by_priority_range(self, start=None, end=None):
        # Finds item objects matching any of priorities.
        # Both 'start' and 'end' priorities are included.
        # This method should work for non numbers priorities.
        if start != None and end != None:
            if start > end:
                err_msg = "Start priority '{}' cant be greater than " +\
                    "end priority '{}'"
                err_msg = err_msg.format(start, end)
                raise ValueError(err_msg)
        def func(_item):
            priority = _item.get_priority()
            if start != None and priority < start:
                return False
            if end != None and priority > end:
                return False
            return True
        return self.filter_items(func)

    def find_items_by_type(self, _type):
        # Finds item objects of specific type.
        # Type is defined as type of object underlying item.
        def func(_item):
            return isinstance(_item.get_object(), _type)
        return self.filter_items(func)    

    def find_objects_by_priority(self, priority):
        # Finds objects within item maching priority.
        items = self.find_items_by_priority(priority)
        return self.extract_objects_from_items(items)
        

    def to_tuple(self):
        # Returns tuple form of block with priorities and objects.
        # Priority will be used as tuple key and object as value.
        # object is the object under reference object of items
        results = []
        for _item in self._items:
            results.append((_item.get_priority(), _item.get_object()))
        return tuple(results)

    def to_dict(self):
        # Returns dict form of block with priorities and objects.
        # This will fail if priority not hashable.
        return dict(self.to_tuple())

    def to_multi_dict(self):
        # Returns multi dict from items priorities and underlying objects.
        # Key is priority and values are underlying objects.
        result_dict = defaultdict(set)
        for _priority, _object in self.to_tuple():
            result_dict[_priority].add(_object)
        return result_dict

    def to_priority_queue(self, maxsize=None):
        # Returns priority queue version of block object.
        # Priority is priority of item object.
        # Value of priority is object underlying item object.
        output_tuple = self.to_tuple()
        if maxsize != None:
            # Slices tuple by maxsize and set queue maxsize.
            output_tuple = output_tuple[:maxsize]
            priority_queue = PriorityQueue(maxsize)
        else:
            # Its better to leave output tuple unchanged and maxsize
            # of queue not set.
            priority_queue = PriorityQueue()
        # Put items(underlying object) into queue with its priority.
        # No way the queue can block while putting items.
        for priority, _object in output_tuple:
            priority_queue.put((priority, _object))
        return priority_queue
    
    def __iter__(self):
        for _priority, _object in self._items():
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
        items = _block.get_items()
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
        self._items = self._to_items(self._items)
        _items = self._extract_deep_items(self)
        # Now asks super class to setup items as usual.
        # Items priorities will be updated as expected.
        super()._setup_items(_items)


if __name__ == "__main__":
    from mimap import reference

    item_object = item.Item(reference.Reference("Ruth"), "b")
    item_object2 = item.Item("Marry", "a")
    item_object3 = item.Item("John", "c")

    items = [item_object, item_object2, item_object3]

    block_object = Block(items)
    deep_object = DeepBlock([Block(items), Block([item.Item("Lord", "aa")], "z")])

    queue_object = deep_object.to_priority_queue()
    print(queue_object.get())
    print(queue_object.get())
    print(queue_object.get())
    print(queue_object.get())
    print(deep_object.extract_objects_from_items(
        deep_object.find_items_by_priority_range()
            ))