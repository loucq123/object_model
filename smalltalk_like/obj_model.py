class Base(object):

    def __init__(self, cls, fields):
        self.cls = cls
        self.fields = fields

    def read_attribute(self, field_name):
        return self.fields.get(field_name)

    def write_attribute(self, field_name, value):
        self.fields[field_name] = value

    def call_method(self, method_name, *args):
        method = self.cls.find_method(method_name)
        return method(self, *args)

    def isinstance(self, cls):
        return self.cls.issubclass(cls)


class Class(Base):

    def __init__(self, name, base_class, fields, metaclass):
        Base.__init__(self, metaclass, fields)
        self.name = name
        self.base_class = base_class

    def super_class_traversal(self):
        if self.base_class is None:
            return [self]
        else:
            return [self] + self.base_class.super_class_traversal()

    def issubclass(self, cls):
        return cls in self.super_class_traversal()

    def find_method(self, method_name):
        for cls in self.super_class_traversal():
            if method_name in cls.fields:
                return cls.fields[method_name]
        return MISSING


class Instance(Base):

    def __init__(self, cls):
        assert isinstance(cls, Class)
        Base.__init__(self, cls, {})

OBJECT = Class(name='object', base_class=None, fields={}, metaclass=None)
TYPE = Class(name='TYPE', base_class=OBJECT, fields={}, metaclass=None)
TYPE.cls = TYPE
OBJECT.cls = TYPE
MISSING = object()

