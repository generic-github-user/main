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

def enum (name : str, variants : str):
    import ast
    print(name, variants)
    src = '\n'.join([
        f'class {name}:',
        '\n'.join(f'    {v} = {i}'
            for i, v in enumerate(variants.split())),
        f'    __variants__ = {variants.split()}'])
    print(src)
    return src
    # return ast.parse(src)
    # exec(src)

exec(enum!(Animal, cat dog fish))
print(Animal)
print(Animal.cat)
