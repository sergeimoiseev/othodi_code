import numpy as np

def func(parts,Lmax=3):
    print('func start')
    print(parts)
    long_parts_remain = False
    for part in parts:
        print("testing len of part")
        print(part)
        if len(part) > Lmax:
            long_parts_remain = True
        # if all([len(part)<=Lmax for part in parts]):
    if not long_parts_remain:
        return parts

    for part in parts:
        if part.shape[0]<=Lmax:
        # if len(part)<=Lmax:
            continue
        else:
            print('this part is too long')
            print(part)
            # i = parts.index(part)
            i = np.where(parts==part)[0][0]
            print('index of this long part')
            print(i)
            rp,lp = part[:part.shape[0]//2], part[part.shape[0]//2:]
            print('part splitted into:')
            print(rp)
            print(lp)
            print('parts to change')
            print(parts)
                    # rp,lp = part[:len(part)//2], part[len(part)//2:]
            # np.put(parts, i, lp)
            # print('parts after put')
            # print(parts)
            parts = np.insert(parts, i, rp )
            print('parts after insert')
            print(parts)
            # parts[i:i+1] = rp,lp
            return func(parts)

def main():
    nodes = (0.,1.,2.,3.,4.,5.)
    indxs = np.array([np.arange(len(nodes),dtype = np.int32)])

    A = np.array([[0, 1, 2,4], [0,3, 2, 0]])
    newrow = [1,2,3]
    A = np.vstack([A, newrow])
    print(A)

    import sys
    sys.exit()
    print(indxs)
    np.put(indxs, 0, [22])
    # np.put(indxs, [2], [22])
    indxs = np.insert(indxs, 2, 11)
    print(indxs)

    # print(indxs)
    # print(indxs[0].shape[0])
    for part in indxs:
        print(part)
        print(part.shape[0])

    # print([part.shape[0]<=5 for part in indxs])


    # indxs = [range(len(nodes))]

    res = func(indxs)
    print('result')
    print(res)

if __name__ == '__main__':
    main()