from mimap import priority

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
    _value_type = priority.Priority
    
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


if __name__ == "__main__":

    item = Item(10, 34)
    item2 = Item(item)
    print(item.get_object())
    print(item.get_priority())