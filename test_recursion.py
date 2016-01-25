
def func(parts,Lmax=1):
    part = parts[0]
    if len(part)<=Lmax:
        return parts
    else:
        rp,lp = part[:len(part)//2], part[len(part)//2:]
        print('new_step')
        print(rp)
        print(lp)
        parts = [rp,lp]+parts[1:]
        return func(parts)

def main():
    parts = [[0,1,2,3,4,5]]
    res = func(parts)
    print('result')
    print(res)

# new_step
# [0, 1, 2]
# [3, 4, 5]
# new_step
# [0]
# [1, 2]
# result
# [[0], [1, 2], [3, 4, 5]]

if __name__ == '__main__':
    main()