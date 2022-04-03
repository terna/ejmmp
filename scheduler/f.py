common='import commonVar as c;'

def f():
    exec(common + 'c.a=1')
