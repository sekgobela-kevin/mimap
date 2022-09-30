# mimap
Mimap is simple python library for associating ordinary python object
with priority. Priority for object helps when sorting and finding the
object. Priority act as key which defines how its object can be accessed.

Mimap allows to get items or sort them based on their their priorities 
instead of the object directly. An object with its priority forms **item**
and multiple items forms **block**. Block also keeps its own priority
which may influence items priorities.

Priorities for items can also influence priority for block. Both items 
and block influence each others priorities. It is possible to have 
nested blocks which is when items of block contain other blocks.

> Priority can be anything than just a number.


### Install
Enter this to your command-line application:
```bash
pip install mimap
```

### Usage

First import mimap to use its functions
```python
import mimap
```

Creates item which is combination of object with its priority. Realise that 
priority can be another type than integer or number. Priority and object
passed to when creating item can accessed using methods. 

Priority for item can be changed and which common when its part of block.

```python
marry_item = mimap.create_item("Marry", 30)
john_item = mimap.create_item("John", 10)
ricky_item = mimap.create_item("Ricky", 40)

marry_item.get_object() # 'Marry'
marry_item.get_priority() # 30

#marry_item.set_priority(20)
#marry_item.get_priority() # 20
```

After creating items you may consider creating block object to hold the 
items. Block makes it easy to work with multiple items such as sorting
or accessing them based on their priorities.

```python
# List of items to use with block
items = [marry_item, john_item, ricky_item]
# Creates block object containing items
items_block = mimap.create_block(items)

items_block.get_priority() # 30
items_block.get_objects() # ['Marry', 'John', 'Ricky']
items_block.get_sorted_objects() # ['John', 'Marry', 'Ricky']

# Gets items by their priorities
item = items_block.get_items_by_priority(30)
item = items_block.get_items_by_priority_range(20,100)

# Gets first and last items based on priority
item = items_block.get_first_item()
item = items_block.get_last_item()
```
> Block object contain even more methods.


It is possible to have nested blocks in that items of block contain another
block. Accessing items within nested block can be hard with previous 
example. But it can be simple if using `mimap.create_deep_block()` instead
of `mimap.create_block()` which does not take into account nested blocks.

```python
# Create first block with items
first_block_items = [marry_item, john_item, ricky_item]
first_block = mimap.create_block(items)

# Create item for second block
first_block_priority = first_block.get_priority()
first_block_item = mimap.create_item(first_block, first_block_priority)

# Create ben item and followed by second block.
# Realise that second block contains first block with items.
ben_item = mimap.create_item("Ben", 100)
second_block_items = [ben_item, first_block_item]
second_block = mimap.create_deep_block(second_block_items)

# Underlying objects from first block can be accessed in second block.
# First block has been eliminated but its items remained.
second_block.get_objects() # ['Ben', 'Marry', 'John', 'Ricky']
second_block.get_sorted_objects() # ['John', 'Marry', 'Ricky', 'Ben']
second_block.get_priority() # 30
```


Priority for block can influence priority for items and vice-verse. If 
priority for block is not provided then it get calculated from priorities
for items. If priority for block is provided then it influences priority for items.

Priority for block was not provided which will cause priority to be 
calculated from items. Priority mode is set to 'mean' which will result in 
priority for block calculated from mean/average of items priorities.

> Non number priorities should rather use 'median' priority mode.

```python
items = [marry_item, john_item, ricky_item]

# Priority for block is not provided and priority_mode set to 'mean'.
# Default priority mode is 'median'.
# Other priority modes can be ('min', 'max')
items_block = mimap.create_block(items, priority_mode="mean")
# This is priorities for each item of block
items_block.get_priorities() # [30, 10, 40]
# This is priority for block
items_block.get_priority() # 26.666666666666668
```

Priority for block was provided and its expected that priority for items
be influnced by priority for block. Priority for item is calculated by 
calculating mean/average of block and item priorities. 

That would mean that new priority of item will be between its original priority and block priority.

> Priorities for items would remain the same for non numbers priorities.

```python
items = [marry_item, john_item, ricky_item]

items_block = mimap.create_block(items, 20, priority_mode="mean")
# Realise that priorities for items changed.
items_block.get_priorities() # [25.0, 15.0, 30.0]
items_block.get_priority() # 20
```

Block can be converted to other python objects like dictionary, tuple 
and priority queue. This only takes into account block items excluding
useful data like block priority.

```python
items = [marry_item, john_item, ricky_item]
items_block = mimap.create_block(items)

items_block.to_tuple() 
# ((10, 'John'), (30, 'Marry'), (40, 'Ricky'))
items_block.to_dict() 
# {10: 'John', 30: 'Marry', 40: 'Ricky'}
items_block.to_multi_dict() 
# {10: {'John'}, 30: {'Marry'}, 40: {'Ricky'}}

# Creates priority queue from block
priority_queue = items_block.to_priority_queue()
priority_queue.get() # (10, 'John')
priority_queue.get() # (30, 'Marry')
```


Most of block methods are available as functions ready to be used on items
without creating block object. 
```python
>>> items = [marry_item, john_item, ricky_item]
>>> mimap.items_to_tuple(items) 
((10, 'John'), (30, 'Marry'), (40, 'Ricky'))
>>> priority_queue = mimap.items_to_priority_queue(items)
>>> priority_queue.get()
(10, 'John')
>>> mimap.extract_objects(items)
['Marry', 'John', 'Ricky']
>>> first_item = mimap.find_first_item(items)
>>> first_item.get_object()
'John'
```

### License
[MIT license](https://github.com/sekgobela-kevin/mimap/blob/main/LICENSE)
