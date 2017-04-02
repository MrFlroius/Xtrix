class Foo:
    def __init__(self, **kwargs):
        for a in kwargs.items():
            setattr(self, a[0], a[1])


f = Foo(a=1, b=2)

print(vars(f))
