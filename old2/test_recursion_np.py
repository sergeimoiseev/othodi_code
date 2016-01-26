import numpy as np


def find_indeces_of_subarray(arr,sub):
    logger.debug("arr\n%s" % (arr,))
    logger.debug("type(arr)\n%s" % (type(arr),))
    logger.debug("sub\n%s" % (sub,))
    logger.debug("type(sub)\n%s" % (type(sub),))
    indices = []
    for el in sub:
        indices.append(arr.index(el))
    return indices

def func(parts,nodes,Lmax=5):
    if all([len(part)<=Lmax for part in parts]):
        return parts
    for part in parts:
        if len(part)<=Lmax:
            continue
        else:
            i = parts.index(part)
            #
            print("part\n%s" % (part,))
            print("i\n%s" % (i,))
            print("s.nodes before extracting\n%s" % (s.nodes,))
            s.nodes = nodes[part]
            print("s.nodes after extracting\n%s" % (s.nodes,))
            logging.disable(logging.DEBUG)
            idx_of_middle = len(part)//2
            new_finish = nodes[idx_of_middle]
            rp,lp = nodes[:idx_of_middle], nodes[idx_of_middle+1:]
            # rp,lp,new_finish = s.split_nodes()
            logging.disable(logging.NOTSET)
            print("len(s.nodes)\n%s" % (len(s.nodes),))
            rp_idxs = find_indeces_of_subarray(s.nodes.tolist(),rp.tolist())
            lp_idxs = find_indeces_of_subarray(s.nodes.tolist(),lp.tolist())
            s.finish = new_finish
            #
            parts[i:i+1] = rp_idxs,lp_idxs
            return func(parts,nodes)


def main():
    nodes_data = np.array([0.,1.,2.,3.,4.,5.,6.,7.,8.])
    parts = [range(len(nodes_data))]
    all_nodes_list = nodes_data#.tolist()
    parts = func(parts,all_nodes_list)
    
    # indxs = [np.arange(len(nodes),dtype = np.int32)]
    # res = func(indxs)
    # print('result')
    # print(res)

if __name__ == '__main__':
    main()