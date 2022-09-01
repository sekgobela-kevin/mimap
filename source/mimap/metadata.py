# Defines metadata class for storing reference metdata.
# Metadata class is similar to dictionary but does not extend one.
# reference.py uses it instead of dictionary.
# source: navaly 0.0.1 (navaly/source/utility/metadata.py)


class Metadata():
    # Defines extra data to be stored on objects
    def __init__(self, metadata={}):
        self.set_metadata(metadata)

    def get_metadata(self, copy=False):
        # Returns copy of metadata
        if copy:
            return self.metadata.copy()
        else:
            return self.metadata

    def set_metadata(self, metadata, overide=True):
        # Overide metadata dictionary with argument
        if isinstance(metadata, dict):
            if overide:
                self.metadata = metadata
            else:
                self.metadata = metadata
        else:
            raise TypeError("Metatada should be dict not", type(metadata))


    def add_data(self, key, value):
        # Add item to metadata
        self.metadata[key] = value

    def get_data(self, key):
        # Access item in metadata
        return self.metadata[key]

    def remove_data(self, key):
        # Removes item in metadata
        del self.metadata[key]

    def data_exists(self, key):
        # Checks if key exists in metadata
        return key in self.metadata

    def get_size(self):
        # Returns the size of metadata
        return len(self.metadata)

    def clear(self):
        # Clears all data in metadata
        self.metadata.clear()
