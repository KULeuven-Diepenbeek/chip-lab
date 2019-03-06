import numpy as np

def findFirstCrossingWithValue(list, value):
    a = []
    for val in list:
        a = np.concatenate((a, [val]))

    idx = np.argwhere(np.diff(np.sign(a - value))).flatten()

    mo_x = list.abscissa[idx[0]].value
    mt_x = list.abscissa[idx[0]+1].value
    mo_y = a[idx[0]].value
    mt_y = a[idx[0]+1].value

    incros_x = ((mt_x-mo_x)/(mt_y-mo_y))*(value-mo_y)+mo_x

    return incros_x, value
