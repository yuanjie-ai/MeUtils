class ParentClass1:
    def __init__(self, arg1, arg11=1):
        self.arg1 = arg1
        self.arg11 = arg11


class ParentClass2:
    def __init__(self, arg2):
        self.arg2 = arg2


class ChildClass(ParentClass1, ParentClass2):
    def __init__(self, arg1, arg2, arg3, **kw):
        ParentClass1.__init__(self, arg1, **kw)
        ParentClass2.__init__(self, arg2)
        self.arg3 = arg3

    def print_args(self):
        print("arg1=", self.arg1)
        print("arg2=", self.arg2)
        print("arg3=", self.arg3)
        print("arg11=", self.arg11)


c = ChildClass("foo", "bar", "baz", arg11=11111111)
c.print_args()
