import unittest

from mimap import block as _block
from mimap import item as _item


class TestBaseBlock(unittest.TestCase):
    _block_type = _block.BaseBlock

    def setUp(self) -> None:
        self._marry_item = _item.Item("Marry", 30)
        self._john_item = _item.Item("John", 10)
        self._ben_item = _item.Item("Ben", 30)
        self._ricky_item = _item.Item("Ricky", 40)

        self._items = [self._marry_item, self._john_item, 
            self._ricky_item, self._ben_item]
        self._sorted_items = sorted(self._items, key=lambda i: i.get_priority())

        self._objects = [item.get_object() for item in self._items]
        self._sorted_objects = [item.get_object() for item in self._sorted_items]
        
        self._priorities = [item.get_priority() for item in self._items]
        self._sorted_priorities = [item.get_priority() for item in self._sorted_items]

        self._tuple = ((item.get_priority(), item.get_object()) 
            for item in self._items)
        self._sorted_tuple = tuple(sorted(self._tuple, key=lambda i:i[0]))
        
        self._block = self._block_type(self._items)

    def test_copy_items(self):
        for item in self._block.copy_items():
            self.assertNotIn(item, self._items)

    def test_get_items(self):
        self.assertCountEqual(self._block.get_items(), self._items)     
    
    def get_objects(self):
        self.assertCountEqual(self._block.get_objects(), self._objects)

    def test_extract_objects_from_items(self):
        objects = self._block_type.extract_objects_from_items(self._items)
        self.assertEqual(objects, self._objects)

    def test_sort_items_by_priority(self):
        items = self._block_type.sort_items_by_priority(self._items)
        self.assertEqual(items, self._sorted_items)

    def test_filter_items(self, key=None, limit=None):
        self.assertEqual(self._block.filter_items(), self._items)
        items = self._block.filter_items(limit=2)
        self.assertEqual(items, self._items[:2])
        items = self._block.filter_items(key=lambda i: i.get_priority()==10)
        self.assertEqual(items, [self._john_item])


class TestBlock(TestBaseBlock):
    _block_type = _block.Block
    _block: _block.Block

    def test_get_sorted_items(self):
        items = self._block.get_items()
        self.assertEqual(items, self._items)

    def test_get_sorted_objects(self):
        sorted_objects = self._block.get_sorted_objects()
        self.assertEqual(sorted_objects, self._sorted_objects)

    def test_get_priorities(self):
        priorities = self._block.get_priorities()
        self.assertEqual(priorities, self._priorities)

    def test_get_items_by_priority(self):
        items = self._block.get_items_by_priority(10)
        self.assertEqual(items, self._sorted_items[:1])

    def test_get_item_by_priority(self):
        item = self._block.get_item_by_priority(10)
        self.assertEqual(item, self._john_item)

    def test_get_items_by_priorities(self):
        items = self._block.get_items_by_priorities([10])
        self.assertEqual(items, self._sorted_items[:1])

    def test_get_item_by_priorities(self):
        item = self._block.get_item_by_priorities([10])
        self.assertEqual(item, self._john_item)

    def test_get_items_by_priority_range(self):
        items = self._block.get_items_by_priority_range(start=10, end=11)
        self.assertEqual(items, self._sorted_items[:1])

    def test_get_item_by_priority_range(self):
        item = self._block.get_item_by_priority_range(start=10)
        self.assertEqual(item, self._items[0])

    def test_get_items_by_type(self):
        items = self._block.get_items_by_type(str)
        self.assertEqual(items, self._items)

    def test_get_item_by_type(self):
        item = self._block.get_item_by_type(str)
        self.assertEqual(item, self._items[0])

    def test_get_first_items(self):
        items = self._block.get_first_items(2)
        self.assertEqual(items, self._sorted_items[:2])

    def test_get_first_item(self):
        item = self._block.get_first_item()
        self.assertEqual(item, self._sorted_items[0])

    def test_get_last_items(self):
        items = self._block.get_last_items(2)
        self.assertEqual(items, self._sorted_items[-2:])

    def test_get_last_item(self):
        item = self._block.get_last_item()
        self.assertEqual(item, self._sorted_items[-1])
        

    def test_to_tuple(self):
        self.assertEqual(self._block.to_tuple(), self._sorted_tuple)

    def test_to_dict(self):
        #self.assertDict(self._block.to_dict(), dict(self._sorted_tuple))
        pass

    def test_to_multi_dict(self):
        for priority, objects in self._block.to_multi_dict().items():
            self.assertIn(priority, self._priorities)
            self.assertTrue(set(objects).issubset(self._objects))

    def test_to_priority_queue(self):
        prority_queue = self._block.to_priority_queue()
        self.assertEqual(prority_queue.get(), (10, 'John'))
        self.assertEqual(prority_queue.get(),(30, "Ben"))
        self.assertEqual(prority_queue.get(), (30, "Marry"))


if __name__ == "__main__":
    unittest.main()