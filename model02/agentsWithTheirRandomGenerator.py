# interactively
# import random
# >>> random.Random
# <class 'random.Random'>


import random as r


class A():
    def __init__(self,r,seed):
        self.r=r.Random()
        self.r.seed(seed)

    def out(self):
        print (self.r.random())

a1=A(r,1)
a2=A(r,2)
a3=A(r,1)

a1.out()
a2.out()
a3.out()

a1.out()
a2.out()
a3.out()

a1.out()
a2.out()
a3.out()

#https://www.adamsmith.haus/python/answers/how-to-declare-a-static-variable-in-a-function-in-python
def f(r,seed):
    if not hasattr(f, "r"):
        f.r=r.Random()
        f.r.seed(seed)
    print (f.__name__,f.r.random())

f(r,1)
f(r,1)
f(r,1)


