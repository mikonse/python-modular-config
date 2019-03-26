import json
from os import path
from threading import RLock


__version__ = '0.2'

SUPPORTED_FORMATS = ['json']


class Config:
    """
    Config object which encapsulates all interactions with the individual config modules and their fields.
    Instantiate like config = Config('config.json')
    """
    def __init__(self, file_path, format='json'):
        if format not in SUPPORTED_FORMATS:
            raise Exception(f'Invalid format for config file. Must be one of {SUPPORTED_FORMATS}')

        self.file_path = file_path
        self.format = format
        self.data = dict()  # module_name:item_name:ConfigField
        self.synced = False
        self._lock = RLock()

    def get(self, module, item):
        """
        Retrieve a config field value for a given module and its field.
        Args:
            module (str): module name
            item (str): config field name

        Returns: Config field value

        """
        if module not in self.data or item not in self.data.get(module):
            raise KeyError(f'Config item {module}:{item} not in config')
        return self.data.get(module).get(item).value

    def set(self, module, item, value):
        """
        Set the value for a config field.
        Additionally synchronizes the config object with the config file.
        Args:
            module (str): module name
            item (str): config field name
            value:  value to be set

        """
        with self._lock:
            if module not in self.data or item not in self.data.get(module):
                raise KeyError(f'Config item {module}:{item} not in config')
            self.data.get(module).get(item).value = value
            self.synced = False
        self.save()

    def __getitem__(self, item):
        # TODO: think about how this would work
        raise Exception('not yet implemented')

    def __setitem__(self, key, value):
        # TODO: think about how this would work
        raise Exception('not yet implemented')

    def register_module(self, module: str, items: list):
        """
        Register a config module with the config object. This takes the module name and a list of config fields of type
        'fields.ConfigField'. After registering a module then config will then be synchronized with the config file,
        meaning the config file will be read and populated with the field defaults if no value is present in the file
        for a given config field.
        Args:
            module (str): module name
            items (list): list of ConfigField objects defining the respective fields

        """
        with self._lock:
            self.data[module] = {item.name: item for item in items}
            self.load()

    def serialize(self, full=False):
        """
        Serialize the complete config into a dictionary. The resulting structure will be a dict with the module names
        as keys and a list of serialized config items as values if 'full=True' or dictionaries containing the config
        field names and values as key-value pairs.

        If 'full' is True, then every config field will be serialized fully, meaning every config field will contain a
        full description with name, value, type, default and all additional attributes.
        Args:
            full (bool): full or compressed serialization

        Returns (dict): serialized config object

        """
        if full:
            return {
                module_name: [item.serialize() for item in module_items.values()]
                for module_name, module_items in self.data.items()
            }

        else:
            return {
                module_name: {
                    item.name: item.value for item in items.values()
                } for module_name, items in self.data.items()
            }

    def serialize_json(self, full=False):
        """
        Same as 'serialize()', but will return a json string instead of a dictionary.
        Args:
            full (bool): full or compressed serialization

        Returns (str): serialized config object as json string

        """
        return json.dumps(self.serialize(full=full))

    def save(self, force=False):
        """
        Synchronize the config object with the config file.
        Args:
            force (bool): if True will force writing to the config file, even if no changes have been made to the config

        Returns (bool): True if successful, False if an error occurred.

        """
        with self._lock:
            if not force and self.synced:
                return True

            try:
                data = self.serialize(full=False)
                if path.isfile(self.file_path):
                    with open(self.file_path, 'r') as f:
                        file_conf = json.load(f)
                        file_conf.update(data)
                        data = file_conf

                with open(self.file_path, 'w+') as f:
                    json.dump(data, f, indent=2)
                self.synced = True
                return True
            except Exception:
                return False

    def update(self, update, full=False):
        """
        Updates the config object with a serialized representation of itself, see 'Config.serialize()' for a detailed
        description. Current values will be overridden by the ones in the update dictionary.
        Args:
            update (dict): serialized representation
            full (bool): full or compressed serialization

        """
        if not isinstance(update, dict):
            raise AttributeError('Expected dict')

        with self._lock:
            for module_name, module in update.items():
                if module_name not in self.data:
                    continue

                if full:
                    for item in module:
                        if item.get('name') in self.data.get(module_name):
                            self.data.get(module_name).get(item.get('name')).value = item.get('value')
                else:
                    for key, value in module.items():
                        if key in self.data.get(module_name):
                            self.data.get(module_name).get(key).value = value
            self.synced = False
        self.save()

    def load(self):
        """
        Populate the config object from the config file.
        Will create and populate the config file with the current config values if none exits.
        """
        if not path.isfile(self.file_path):
            self.save(force=True)
            return True

        with self._lock:
            with open(self.file_path, 'r') as f:
                file_conf = json.load(f)  # TODO: maybe catch exception?
                self.update(file_conf, full=False)
                return True
