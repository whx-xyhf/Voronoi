import numpy as np
from scipy import stats

""" 生成核密度矩阵 （耗时长） """
def calcu_kde(loc_array):

    loc_array = np.array(loc_array)
    m1 = loc_array[:, 0]
    m2 = loc_array[:, 1]
    xmin = m1.min()
    xmax = m1.max()
    ymin = m2.min()
    ymax = m2.max()
    X, Y = np.mgrid[xmin: xmax: 2, ymin: ymax: 2]

    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    try:
        kernel = stats.gaussian_kde(values)
    except:
        print(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    kde = [kernel([p[0], p[1]])[0] for p in loc_array]
    m4 = np.asarray(kde)

    return kde
