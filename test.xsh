def Echo (x : str):
    print(x)
    return x

Echo!(hello)

# def Echo2 (x : list[str]):
# def Echo2 (*x : str):
def Echo2 (x):
    # print(list(x))
    print(x.split())
    return x
Echo2!(a b c)
