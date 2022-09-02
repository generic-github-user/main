def subdivide(num, parts):
    result = []
#     while num>0:
    factor = max(1/p for p in parts)
    parts = [int(p*factor) for p in parts]
    num *= factor
    parts.sort(reverse=True)
    for p in parts:
#             while num>p:
        if num >= p:
            x = num // p
            result.append((p/factor, x))
            num -= p * x
    if num:
        print(f'Remainder of {round(num/factor, 4)}')
    return result


