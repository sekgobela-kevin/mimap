from mimap import item
from mimap import priority as priority_mod

from collections import defaultdict
from queue import PriorityQueue


class BaseBlock():
    '''Base class for block block objects.
    
    Intances of this class wont modify or perform any operation on
    items as compared to Block class. It comes handy for implementing
    block class for creating block objects.'''
    def __init__(self, items, _type=object) -> None:
        self._items = items
        self._type = _type

    def _to_items(self, _items_like):
        # Returns item objects from iterator of objects.
        # Item objects will be returned unchanged.
        # Non item objects will  result in item objects.
        return  [item.Item.to_item(_item) for _item in _items_like]

    def copy_items(self):
        # Copies current items of block
        return [self._item.copy() for _item in self._items]

    def get_items(self):
        # Returns items stored in block object
        return self._items
    
    def get_objects(self, priority_sort=False):
        '''Gets items underlying objects'''
        return self.extract_objects_from_items(self._items)

    @classmethod
    def extract_objects_from_items(cls, items):
        '''Gets underlying object from item object'''
        return [_item.get_object() for _item in items]

    @classmethod
    def sort_items_by_priority(cls, items):
        '''Returns items sorted by their priorities'''
        return sorted(items, key=lambda _item: _item.get_priority())

    def filter_items(self, key=None, limit=None):
        '''Filters item objects filtered by key function'''
        filtered_items = list(filter(key, self._items))
        if limit != None:
            filtered_items = filtered_items[:limit]
        return filtered_items

    def __iter__(self):
        return iter(self.get_sorted_items())

    def __len__(self):
        return len(self._items)


class Block(BaseBlock):
    '''Wraps collection of Item objects and associate them with priority.
    
    Instances of this class first copies each item before performing
    any operation on them. Priority for item can influence priority
    for block instance if priority for block is not provided.
    
    Priority for block also has impact priority for each item. Items and
    block instance influence each other priorities in some way. Thats 
    items are first copies to avoid changing priorities of original items.
    
    `priority_mode` can be used to control how priority of items can 
    influence priority of block or vice-verse. Median is used by default
    as it can be used on non numbers priority unlike mean/average. 
    
    Setting `update_priorities` to False would result in items priorities
    not influenced by block priority and not copied. Setting priority for 
    block would result in block not infuenced by items priorities.
    
    When `strict` is True, block instance will not allow item containing
    another block. This is by default set to True to avoid confusion
    but can be set to True to allow nested block instances.'''
    # Default priority when priority not provided.
    _default_priority = item.Item.get_default_value()

    def __init__(self, items, priority=_default_priority, _type=object, 
    strict=True, priority_mode=None, update_priorities=True):
        '''
        items: Iterator
            Collection of Item objects
        priority: Any
            Any object can sorted or support comparison operators.   
            It needs to be compatible with items priorities unless 
            `update_priorities` is False.
        _type: Type
            Type of items this block expectes, default: object
        strict: Bool
            Prevents block from containing items containing other blocks.
        priority_mode: Str
            Mode for calculating priority for block and items, default:
            'median'.
        update_priorities: Bool
            Enables and disables updating of block and items priorities.
        '''
        super().__init__(items, _type)
        self._items = items
        self._strict = strict
        self._type = _type
        self._strict = strict
        self._update_priorities = update_priorities
        # Calling methods with initializer causes problems.
        # Thats why super().__init__() is fist call to __init__().
        self._setup_priority_mode(priority_mode)
        # priority_mode need to be setup before setting priority.
        # This will cause problems when methods are overiden.
        # Priority for this block may be changed.
        self._setup_priority(priority)
        # Setup items after priority have been set from existing items.
        # The method may modify priorities for items.
        # Priority is passed as argument since priority argument may
        # have been modified.
        # This are results of calling methods within initialiser.
        self._setup_items(items, priority)
        # Calling method within initializer is hell.
        # The instance is not yet fully created.
        # Warning has been included on the methods called by __init__().

    def _setup_priority(self, priority):
        # Setup priority from average of items priorities.
        # Default priority is already set by super class.
        # This method is not meant to be overiden(take care)
        if priority == self._default_priority:
            # Priority was suppossed to be calculated from average.
            # But priority can be non number(that makes it impossible).
            # Median is used here to calculate priority for block.
            # That allows non numbers to be used as priority without error.
            priorities = [_item.get_priority() for _item in self._items]
            # Empty priorities wont work(rather be default one)
            if priorities:
                if self._priority_mode in self._median_priority_modes:
                    # Calculates priority from median(midpoint).
                    # This is based on position other than values.
                    # It will work even if priorities are non numbers.
                    priorities.sort(reverse=False)
                    # Get midpoint index of priorities list
                    median_index = round((len(priorities)-1)/2)
                    # Use the index to find meadin priority.
                    _priority = priorities[median_index]
                elif self._priority_mode in self._average_priority_modes:
                    # Calculates avarage of priorities.
                    # Priorities needs to be numbers to work.
                    _priority = sum(priorities)/len(priorities)
                elif self._priority_mode in self._min_priority_modes:
                    # Minumum of priorities is used as block priority.
                    _priority = min(priorities)
                elif self._priority_mode in self._max_priority_modes:
                    # Maximum of priorities is used as block priority.
                    _priority = max(priorities)
                else:
                    err_msg = "priority_mode should one of {} not '{}'"
                    err_msg = err_msg.format(
                        self._priority_modes, 
                        self._priority_mode
                    )
                    raise ValueError(err_msg)
                self._priority = _priority
            else:
                # No way priority can be calculated without items.
                # Priority may need to be set explicity in initializer.
                err_msg = "There are no items to calculate block priority"
                raise ValueError(err_msg)
        else:
            self._priority = priority

    def _setup_items(self, items, priority):
        # Setup items to ensure they are in correct type.
        # Item objects will be created when neccessary.
        # This could make find bugs hard but it simplifies things.
        # This method is not meant to be overiden(take care)
        new_items = []
        for _item in items:
            new_item = item.Item.to_item(_item)
            # Gets object underlying item.
            _object = new_item.get_object()
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
        if self._update_priorities and priority != None:
            # Copies items to avoid modifying original ones.
            copied_items = [_item.copy() for _item in new_items]
            self._items = self._update_items_priorities(copied_items,
            priority)
        else:
            self._items = new_items

    def _setup_priority_modes(self):
        # Setup possible values of priority mode.
        self._average_priority_modes = {"average", "avg", "mean"}
        self._median_priority_modes = {"median"}
        self._min_priority_modes = {"min"}
        self._max_priority_modes = {"max"}
        self._priority_modes = {
            *self._average_priority_modes,
            *self._median_priority_modes,
            *self._min_priority_modes,
            *self._max_priority_modes
        }

    def _setup_priority_mode(self, priority_mode):
        # This method is not meant to be overiden(take care)
        self._setup_priority_modes()
        if priority_mode == None:
            # Median is by default used to calculate block priority.
            # Median is better as it works with non numbers.
            self._priority_mode = list(self._median_priority_modes)[0]
        else:
            self._priority_mode = priority_mode

    def _update_items_priorities(self, items, block_priority):
        # Updates items priorities with ones calculated from block priority.
        if block_priority == self._default_priority:
            # No updating items priorities when block priority is not
            # provided(being None).
            return items
        updated_items = []
        for _item in items:
            # Copies item object(avoid modifying original object)
            new_item_priority =  _item.get_priority()
            if self._priority_mode in self._average_priority_modes:
                # New priority is between item and block priorities.
                # Average is the best as it satisfies both block and item 
                # priorities equally.
                new_priority = (self._priority + new_item_priority)/2
                _item.set_priority(new_priority)
            updated_items.append( _item)
        return updated_items

    def _should_update_block_priority(self):
        # Checks if block priority should be updated.
        # Method not reliabe as priority can be modified on initialiser.
        return self._update_priorities and self._priority ==\
             self._default_priority

    def _should_update_items_priorities(self):
        # Checks if block priority should be updated.
        # Method not reliabe as priority can be modified on initialiser.
        return self._update_priorities and self._priority != None

    @classmethod
    def sort_items_by_priority(cls, items):
        '''Returns items sorted by their priorities'''
        return sorted(items, key=lambda _item: _item.get_priority())

    def set_priority(self, priority):
        '''Sets priority for block and update items priorities'''
        self._priority = priority
        self._items = self._get_items_with_new_priorities(self._items) 

    def get_priority(self):
        '''Gets priority for block'''
        return self._priority

    def get_sorted_items(self):
        '''Gets items sorted by their priorities'''
        return self.sort_items_by_priority(self._items)

    def get_sorted_objects(self):
        '''Gets items underlying objects sorted by priority'''
        sorted_items = self.get_sorted_items()
        return self.extract_objects_from_items(sorted_items)

    def get_priorities(self):
        '''Gets priorities of block item objects'''
        return [_item.get_priority() for _item in self._items]

    def get_items_by_priority(self, priority):
        '''Gets item objects matching priority'''
        def func(_item):
            return _item.get_priority() == priority
        return self.filter_items(func)

    def get_item_by_priority(self, priority):
        '''Gets first item matching priority'''
        items = self.get_items_by_priority(priority)
        if items: return items[0]

    def get_items_by_priorities(self, priorities):
        '''Gets item objects matching any of priorities'''
        def func(_item):
            return _item.get_priority() in priorities
        return self.filter_items(func)

    def get_item_by_priorities(self, priorities):
        '''Gets first item matching any of priorities'''
        items = self.get_items_by_priorities(priorities)
        if items: return items[0]

    def get_items_by_priority_range(self, start=None, end=None):
        '''Gets item objects with priorities in range'''
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

    def get_item_by_priority_range(self, start=None, end=None):
        '''Gets first item with priority in range'''
        items = self.get_items_by_priority_range(start, end)
        if items: return items[0]

    def get_items_by_type(self, _type):
        '''Gets item objects of provided type'''
        # Type is defined as type of object underlying item.
        def func(_item):
            return isinstance(_item.get_object(), _type)
        return self.filter_items(func)   

    def get_item_by_type(self, _type):
        '''Gets first item of provided type'''
        items = self.get_items_by_type(_type)
        if items: return items[0] 

    def get_first_items(self, limit=3):
        '''Gets first item objects based on their priority'''
        sorted_items = self.sort_items_by_priority(self._items)
        return sorted_items[:limit]

    def get_first_item(self):
        '''Gets first item based on priority'''
        items = self.get_first_items(1)
        if items: return items[0]

    def get_last_items(self, limit=3):
        '''Gets last item objects based on their priority'''
        sorted_items = self.sort_items_by_priority(self._items)
        return sorted_items[-limit:]

    def get_last_item(self):
        '''Gets last item based on priority'''
        items = self.get_last_items(1)
        if items:
            return items[-1]
        

    def to_tuple(self):
        '''Returns tuple form of block with priorities and objects'''
        # Priority will be used as tuple key and object as value.
        # object is the object under reference object of items
        results = []
        for _item in self.get_sorted_items():
            results.append((_item.get_priority(), _item.get_object()))
        return tuple(results)

    def to_dict(self):
        '''Returns dict form of block with priorities and objects'''
        # This will fail if priority not hashable.
        return dict(self.to_tuple())

    def to_multi_dict(self):
        '''Returns multi dict from items priorities and underlying objects'''
        # Key is priority and values are underlying objects.
        result_dict = defaultdict(set)
        for _priority, _object in self.to_tuple():
            result_dict[_priority].add(_object)
        return result_dict

    def to_priority_queue(self, maxsize=None):
        '''Returns priority queue version of block object'''
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


class DeepBlock(Block):
    ''' Varient of Block that allows extracting of deep/low-level items.

    This block class differs from its parent in that it eliminates
    nested block instances by extracting their items and then removing
    any item that contain block instances.
    
    At end of day, items with block instances are removed while retaining
    their items. This class gurantees that its items wont have any block
    object. That makes it easy to access items that were deep into nested
    block objects.
    
    `strict` is now set to False as this block type is based on nested 
    block objects. One should now not fear to nest block objects together
    within item objects that will be used on another block object.
    
    Priorities for block and items will be updated accordinly as similar
    to its parent class.'''
    
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

    def _setup_items(self, items, priority):
        # Setup deep items overiding existing item objects.
        # Ensures all items are really item objects.
        # _extract_deep_items() expectes item objects.
        self._items = self._to_items(self._items)
        _items = self._extract_deep_items(self)
        # Now asks super class to setup items as usual.
        # Items priorities will be updated as expected.
        super()._setup_items(_items, priority)


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
    print("block priority: ", block_object.get_priority())
    print("deep_block priority: ", deep_object.get_priority())