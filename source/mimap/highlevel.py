from mimap import block
from mimap import item



__all__ = [
    "create_item",
    "create_block",
    "create_deep_block",
    "create_mapping",

    "items_to_priority_queue",
    "items_to_map_tuple",
    "items_to_dict",

    "flatten_items",
    "extract_objects",
    "sort_items_by_priority",

    "find_items_by_priorities",
    "find_item_by_priorities",

    "find_items_by_priority_range",
    "find_item_by_priority_range",

    "find_items_by_type",
    "find_item_by_type",

    "find_first_items",
    "find_first_item",

    "find_last_items",
    "find_last_item"
]

def create_item(_object, priority, **kwargs):
    '''Creates item object containing object and its priority.'''
    return item.Item(_object, priority, **kwargs)

def create_block(items, **kwargs):
    '''Creates block object with priority from items.  
    
    If items contains block object consider using `create_deep_block()`
    as it will extract the items of that block. Continue using this
    function if thats what you want.'''
    return block.Block(items, **kwargs)

def create_deep_block(items, **kwargs):
    '''Creates deep block object from items.  
    
    Deep block is neccessay when items can contain block object
    which may contain other items. This function results in block object
    that contain other items extracted. Any nested block objects within
    items get removed while retaining non block items.
    
    This is different from `create_block()` as it keeps items containing
    block object. That makes it harder to access deep or low-level items
    within the nested block objects.

    Note that extracted deep/low-level items are only copies of original.
    Block object first copies items before performing anything on them.
    Getting items throuh `.get_items()` will only return the copies.
    '''
    return block.DeepBlock(items, **kwargs)


def create_mapping(items, flatten=False, **kwargs):
    '''Creates corresponding block object based on 'flatten' argument.

    When 'flatten' is True, `create_block()` will be used to create 
    block object else `create_deep_block()`. Set 'flatten' argument to 
    True to remove any nested block objects and replace them with their 
    items.
    '''
    if flatten:
        return create_deep_block(items, **kwargs)
    else:
        return create_block(items, **kwargs)


######################################################################
# Functions defined after here internally creates block object.
# It may be better to manually create block object for performance.
# These functions are meant to give functional programming flavour.
# Manually creating block object could result in few more advantages.
######################################################################

def items_to_priority_queue(items, flatten=False):
    '''Convert items into priority queue'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.to_priority_queue()

def items_to_map_tuple(items, flatten=False):
    '''Convert items into map like tuple'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.to_tuple()

def items_to_dict(items, flatten=False):
    '''Convert items into multi dict'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.to_dict()



def flatten_items(items):
    '''Flattens items by exposing items within nested block objects.
    
    This function removes any block object within items while retaining
    items. The number of resulting items may be larger than items 
    provided on argumnets. This is because this function exposes items
    that were nested deep within block objects.
    
    This function does not affect nested items but items containing
    block. Nested items is something out of scope of this library but block
    and items can be nested.

    Block can contain items containing other blocks and items can contain
    block objects. But items containg other items is something that wasnt
    planned for this library.
    '''
    block_object = create_deep_block(items, update_priorities=False)
    return block_object.get_items()

def sort_items_by_priority(items):
    '''Sorts items based on their priorities'''
    block_object = create_block(items, update_priorities=False,
    strict=False)
    return block_object.get_sorted_items()

def extract_objects(items, flatten=False):
    '''Extracts objects within items'''
    #return [_item.get_object() for _item in items]
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_objects()



def find_items_by_priorities(items, priorities, flatten=False):
    '''Finds items with priorities matching any of priorities'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_items_by_priorities(priorities)

def find_item_by_priorities(items, priorities, flatten=False):
    '''Finds item with priority matching any of priorities'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_item_by_priorities(priorities)


def find_items_by_priority_range(items, start=None, end=None, flatten=False):
    '''Finds items with priorities in ramge'''
    block_object = create_mapping(items, start=None, end=None, 
    flatten=flatten, strict=False)
    return block_object.get_items_by_priority_range(start, end)

def find_item_by_priority_range(items, start=None, end=None, flatten=False):
    '''Finds item with priority in ramge'''
    block_object = create_mapping(items, start=None, end=None, 
    flatten=flatten, strict=False)
    return block_object.get_item_by_priority_range(start, end)


def find_items_by_type(items, _type, flatten=False):
    '''Finds items with type matching provided type'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_items_by_type(_type)

def find_item_by_type(items, _type, flatten=False):
    '''Finds item with type matching provided type'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_item_by_type(_type)


def find_first_items(items, limit=3, flatten=False):
    '''Finds first items by priority'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_first_items(limit)

def find_first_item(items, flatten=False):
    '''Finds the first item by priority'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_first_item()


def find_last_items(items, limit=3, flatten=False):
    '''Finds last items by priority'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_last_items(limit)

def find_last_item(items, flatten=False):
    '''Finds the last item by priority'''
    block_object = create_mapping(items, flatten=flatten, strict=False)
    return block_object.get_last_item()
