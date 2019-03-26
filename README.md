# Modular-Config

**modular-config** is a python package designed to make dynamic configuration inside a python 
project as easy as possible. It follows a modular approach, meaning if you have a project
containing several modules that each have parameters you'd like to be able to configure in
a central location, e.g. a config file while still being able to have the definition of those 
configuration parameters self contained in those individual modules then you've come to the
right place. 

# Usage
## Getting started
First create a central config object that holds the whole configuration and synchronizes 
itself with the config file.
```python
from modular_conf import Config

config = Config('config.json')
```
You are now able to register a module with the configuration.
Create a list of config fields you want to have and register them under a module name.
```python
from modular_conf.fields import BoolField, StringField

fields = [
    BoolField(name='field1', default=False),
    StringField(name='field2', default='Sample')
]

config.register_module('your_module_name', fields)
```
After registering the fields the config will synchronize with the config file. If the file is not present
it will be created and if some field values are not yet contained in the config file it will be populated with
the given defaults.
In our case if no config file existed previously so a new one was created and looks as follows:
```json
{
  "your_module_name": {
    "field1": false,
    "field2": "Sample"
  }
}
```
The config can be accessed in your module and field values can be read and set via:
```python
config.get('your_module_name', 'field1')
config.set('your_module_name', 'field2', 'new value')
```
Since each individual field was defined with a given type the config will automatically validate each field and raise
an error if a type mismatch occurs. For example calling
```python
config.set('your_module_name', 'field2', False)
``` 
Will raise an error as `field2` was defined as a `StringField`.

## List of avaiable config field types
- *IntField*  - Simple integer
- *StringField*  - Simple string
- *BoolField*  - Simple boolean
- *ChoiceField*  - Field with a given set of possible choices (may be any type)
- *ListField*  - contains an arbitrary list
- *TupleListField*  - Contains a list of tuples. The tuples have a predefined length and have 
associated names for each tuple element. E.g. a list of IP address, MAC address pairs. Tuple element names
improve readability and can be used in a frontend to render the config field.
- *DictField*  - contains an arbitrary dictionary

# Installation
Simply
```bash
pip install modular-conf
```

# Contribution
Feel free open pull requests. Contributions of any form are appreciated deeply!