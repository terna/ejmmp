# interactively
# import random
# >>> random.Random
# <class 'random.Random'>


import random

R=random.Random

class A():
    def __init__(self,r,seed):
        self.r=r
        self.r.seed(seed)

    def out(self):
        print (self.r.random())

a1=A(R(),1)
a2=A(R(),2)
a3=A(R(),1)

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
    if not hasattr(f, "rr"):
        f.rr=r
        f.rr.seed(seed)
    print (f.__name__,f.rr.random())

f(R(),1)
f(R(),1)
f(R(),1)


