import json


class InvalidTypeException(Exception):
    pass


class ConfigField:
    def __init__(self, name, default, type):
        self.name = name
        self.default = default
        self.type = type
        self.value = default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.validate(value):
            raise InvalidTypeException(
                f'Invalid type for config field. Expected {self.type}, got {type(value)} for {value}')
        self._value = value

    def validate(self, v):
        if not isinstance(v, self.type):
            return False
        return True

    def serialize(self):
        return {
            'name': self.name,
            'type': self.type_to_string(),
            'default': self.default,
            'value': self.value
        }

    def type_to_string(self):
        return str(self.type)

    def serialize_json(self):
        return json.dumps(self.serialize())


class BoolField(ConfigField):
    def __init__(self, name, default):
        super().__init__(name, default, bool)

    def type_to_string(self):
        return 'bool'


class StringField(ConfigField):
    def __init__(self, name, default):
        super().__init__(name, default, str)

    def type_to_string(self):
        return 'str'


class IntField(ConfigField):
    def __init__(self, name, default):
        super().__init__(name, default, int)

    def type_to_string(self):
        return 'int'


class ChoiceField(ConfigField):
    def __init__(self, name, default, choices: tuple, type):
        self.choices = choices  # needs to be assigned before super call for validate to work properly
        super().__init__(name, default, type)

        if default not in self.choices or not all([isinstance(i, self.type) for i in self.choices]):
            raise InvalidTypeException(
                f'Choices provided to choice field ({self.choices}) do not match given type ({self.type})')

    def validate(self, v):
        if v not in self.choices:
            return False
        return True

    def serialize(self):
        sup = super().serialize().copy()
        sup.update({
            'choices': self.choices,
        })
        return sup

    def type_to_string(self):
        return 'choice'


class ListField(ConfigField):
    def __init__(self, name, default):
        super().__init__(name, default, list)

    def type_to_string(self):
        return 'list'


class TupleListField(ListField):
    def __init__(self, name, default, n_elems, element_names: tuple):
        super().__init__(name, default)
        self.n_elems = n_elems
        self.elem_names = element_names

    def validate(self, v):
        if not isinstance(v, self.type):
            for i in v:
                if not isinstance(i, (list, tuple)) or len(i) != self.n_elems:
                    return False
        return True

    def serialize(self):
        sup = super().serialize().copy()
        sup.update({
            'n_elems': self.n_elems,
            'elem_names': self.elem_names
        })
        return sup

    def type_to_string(self):
        return 'tuple_list'


class DictField(ConfigField):
    def __init__(self, name, default):
        super().__init__(name, default, dict)

    def type_to_string(self):
        return 'dict'
