class SlotsClass:
    __slots__ = ('foo', 'baz')
    


s = SlotsClass()
s.foo = 'foo'
s.baz = 'baz'
s.some_other = 'q'  # AttributeError: 'SlotsClass' object has no attribute 'some_other'
