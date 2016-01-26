import numpy
def min_and_idxs(np_arr):
    upper_tri = np.triu(np_arr)
    m_a = np.ma.masked_equal(upper_tri, 0.0, copy=False)
    idxs_min_T = np.where(m_a == m_a.min())
    idxs_min = np.asarray(idxs_min_T).T
    idxs_min_tuples = [tuple(idx_pair) for idx_pair in idxs_min]
    # print(idxs_min_tuples)
    # return {'min':np_arr[idxs_min_tuples[0]], 'idxs':idxs_min_tuples}
    try:
        return {'min':np_arr[idxs_min_tuples[0]], 'idxs':idxs_min_tuples[0]}
    except IndexError:
        return {'min':0, 'idxs':[(0,0)]}

def mask_from_index(np_arr,idx):
    shape = np_arr.shape
    m_a_i = np.fromfunction(lambda i, j: i==idx, shape, dtype=int)
    m_a_j = np.fromfunction(lambda i, j: j==idx, shape, dtype=int)
    # m_a_i = np.fromfunction(lambda i, j: i>idx, shape, dtype=int)
    # m_a_j = np.fromfunction(lambda i, j: j>idx, shape, dtype=int)
    m_a_or = np.ma.mask_or(m_a_i,m_a_j)
    return np.ma.masked_array(np_arr, np.logical_not(m_a_or))  # creates a copy
