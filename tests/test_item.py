import unittest

from mimap import item as _item


class TestItem(unittest.TestCase):
    def setUp(self) -> None:
        self.object = "age"
        self._priority = 12
        self._priority_callable = lambda: self._priority
        self._item = _item.Item(self.object, self._priority)
        self._item_callable = _item.Item(self.object, self._priority_callable)
    
    def test_get_priority(self):
        self.assertEqual(self._item.get_priority(), self._priority)
        self.assertEqual(self._item_callable.get_priority(), self._priority)

    def test_set_priority(self):
        self._item.set_priority(False)
        self.assertEqual(self._item.get_priority(), False)

    def test_get_object(self):
        self.assertEqual(self._item.get_object(), self.object)


if __name__ == "__main__":
    unittest.main()
