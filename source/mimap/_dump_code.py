from queue import PriorityQueue
from mimap.priority import Priority

import pemap


class Item(pemap.Item):
    '''Associates reference object with priority.
    
    Instances of this class store a reference containing object 
    and associate it with priority. If non non reference object
    is passed as reference, reference object will be created form it.
    
    Priority defines priority of reference over other references. Its 
    most likely to be a number but can be any python object. The smaller
    priority value the higher reference will have priority over other 
    references.
    
    Remember that this class internally creates reference object if 
    reference argument is not Reference object.'''
    _value_attrs = ("priotity", "get_priority") 
    _value_type = Priority
    
    def __init__(self, _reference, priority=None, *args, **kwargs):
        '''
        _reference: Reference
            Instance of Reference type or any python object.
        priority: Any
            Any object can sorted or support comparison operators.   
        _type: Type
            Type of reference item expectes, default: object.
        strict: Bool
            Forces `_reference` argumnet to be strictly Reference instance.
        '''
        super().__init__(_reference, priority, *args, **kwargs) 

    def get_priority(self):
        '''Gets priority of this object'''
        return self._value.get_value()

    def set_priority(self, priority):
        '''Gets priority priority for this object'''
        self._value.set_value(priority)




class Block(pemap.Block):
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
    "_default_priority = Item.get_default_value()"

    # Setups priority modes
    _average_priority_modes = {"average", "avg", "mean"}
    _median_priority_modes = {"median"}
    _min_priority_modes = {"min"}
    _max_priority_modes = {"max"}
    _priority_modes = {
        *_average_priority_modes,
        *_median_priority_modes,
        *_min_priority_modes,
        *_max_priority_modes
    }

    def __init__(self, items, priority="_default_priority", _type=object, 
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
        self._update_priorities = update_priorities
        # Calling methods with initializer causes problems.
        self._setup_priority_mode(priority_mode)
        # priority_mode need to be setup before setting priority.
        # This will cause problems when methods are overiden.
        # Priority for this block may be changed.
        self._setup_priority(priority)
        # Calling method within initializer is hell.
        # The instance is not yet fully created.
        # Warning has been included on the methods called by __init__().
        super().__init__(items, _type, strict)

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

    def _setup_items(self, items):
        # Setup items to ensure they are in correct type.
        # Item objects will be created when neccessary.
        # This could make find bugs hard but it simplifies things.
        # This method is not meant to be overiden(take care)
        super()._setup_items(items)

    def _setup_priority_mode(self, priority_mode):
        # This method is not meant to be overiden(take care)
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
