class A():

    def __init__(self,c):
        self.c=c

    def set_a(self,a):
        self.a=a

    def get_a(self):
        return self.a

    def print_self(self):
        print(self)


a1=A(3)
a2=A(33)

a1.set_a(1)
a2.set_a(2)


print (a1.get_a() )
print (a2.get_a() )


"""
Try:

>>> A

>>> a1

>>> a2

>>> get_a

>>> A.get_a

>>> A.get_a()

>>> A.get_a(a1)

>>> A.b=3

>>> a1.b


"""
