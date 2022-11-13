from lib.pystring import String


# one day I will pay for my sins
def If(p, x, y):
    if p:
        return x()
    else:
        return y()
