import numpy as np

n_steps = 0
def func(parts,Lmax=1):
    global n_steps
    # part = parts[0]
    print('step into recursion')
    print(parts)
    if all([len(part)<=Lmax for part in parts]):
        print('recursion floor')
        return parts
    if n_steps > 6:
        print('hard stop recursion')
        return False

    for part in parts:
        if len(part)<=Lmax:
            print(part)
            print('continuing')
            continue
        else:
            print(part)
            print('new_step %d' % n_steps)
            i = parts.index(part)
            rp,lp = part[:len(part)//2], part[len(part)//2:]
            n_steps += 1
            parts[i:i+1] = rp,lp
            # parts = [rp,lp]+parts[1:]
            return func(parts)

def main():
    nodes = (0.,1.,2.,3.,4.,5.)
    indxs = [range(len(nodes))]
    res = func(indxs)
    print('result')
    print(res)

if __name__ == '__main__':
    main()