import unittest
import mimap


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        marry_item = mimap.create_item("Marry", 30)
        john_item = mimap.create_item("John", 10)
        ricky_item = mimap.create_item("Ricky", 40)

        # List of items to use with block
        items = [marry_item, john_item, ricky_item]
        items_block = mimap.create_block(items)