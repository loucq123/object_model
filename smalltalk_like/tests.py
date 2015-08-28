from obj_model import Class, Instance, TYPE, OBJECT


def test_creation():
    test_attribute()
    test_subclass()
    test_callmethod()


def test_attribute():

    # Python Code
    class A(object):
        pass

    obj = A()
    obj.a = 1
    assert obj.a == 1

    obj.b = 2
    assert obj.b == 2

    obj.a = 3
    assert obj.a == 3

    # Object Model Code
    A = Class(name='A', base_class=OBJECT, fields={}, metaclass=TYPE)
    obj = Instance(A)

    obj.write_attribute('a', 1)
    assert obj.read_attribute('a') == 1

    obj.write_attribute('b', 2)
    assert obj.read_attribute('b') == 2

    obj.write_attribute('a', 3)
    assert obj.read_attribute('a') == 3


def test_subclass():

    # Python Code
    class A(object):
        pass

    class B(A):
        pass

    obj_b = B()
    assert isinstance(obj_b, B) and isinstance(obj_b, A) and isinstance(obj_b, object)
    assert not isinstance(obj_b, type)

    # Object Model Code
    A = Class(name='A', base_class=OBJECT, fields={}, metaclass=TYPE)
    B = Class(name='B', base_class=A, fields={}, metaclass=TYPE)
    obj_b = Instance(B)
    assert obj_b.isinstance(B) and obj_b.isinstance(A) and obj_b.isinstance(OBJECT)
    assert not obj_b.isinstance(TYPE)


def test_callmethod():

    # Python Code
    class A(object):

        def m1(self):
            return self.a

        def m2(self, n):
            return self.a + n

    obj = A()
    obj.a = 1
    assert obj.m1() == 1
    assert obj.m2(3) == 4

    # Object Model Code
    def m1_A(self):
        return self.read_attribute('a')

    def m2_A(self, n):
        return self.read_attribute('a') + n

    A = Class(name='A', base_class=OBJECT, fields={'m1_A': m1_A, 'm2_A': m2_A}, metaclass=TYPE)

    obj = Instance(A)
    obj.write_attribute('a', 1)
    assert obj.call_method('m1_A') == 1
    assert obj.call_method('m2_A', 3) == 4


if __name__ == '__main__':
    test_creation()