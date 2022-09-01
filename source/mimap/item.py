# Defines Item class which wraps reference object along with its metadata.
# Item class also implements Priority so that it instancescan be used in 
# place of reference object or vice-verse.
# Reference can be used without Item object as it has its own priority.
# Item gives oportunity to overide that priority and metadata support.

from mimap import metadata
from mimap import reference


class Item(reference.Priority):
    # Links reference object to metadata and priority.
    # Item has precidence over reference own priority.
    def __init__(self, _reference, _metadata={}, priority_callable=None):
        super().__init__(None) # priority not available at moment
        self.__setup_reference(_reference)
        self.__setup_metadata( _metadata)
        self._priority_callable = priority_callable
        self.__setup_priority(None) # priority not available at moment


    def __setup_priority(self, priority):
        # Setup priority from metadata, priority callable or reference.
        if self._priority_callable:
            # Sets priority from priority callable.
            self._priority = self._priority_callable(self._metadata)
        elif self._metadata.data_exists("priority"):
            # Sets priority from metadata.
            self._priority = self._metadata.get_data("priority")
        else:
            # Priority is not available, set priority from reference.
            self._priority =  self._reference.get_priority()

    def __setup_reference(self, _reference):
        # Creates reference object when neccessay
        if isinstance(_reference, reference.Reference):
            self._reference = _reference
        else:
            self._reference = reference.Reference(_reference)

    def __setup_metadata(self, _metadata):
        # Creates Metadata object when neccessary
        if isinstance(_metadata, dict):
            self._metadata = metadata.Metadata(_metadata)
        else:
            # Its responsibility of developer to ensure metadata
            # argument is in correct types(dict or metadata.Metadata)
            self._metadata = _metadata

    def get_reference(self):
        # Returns underling reference object
        return self._reference


if __name__ == "__main__":

    item = Item(10)
    print(item.get_priority())