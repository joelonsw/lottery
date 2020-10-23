from lotteryapp.models import *
from user.models import *

# numpy ver 1.19.2
import numpy as np

class LinearFitting:

    def __init__(self, name):
        self.item = name
        self.slope = None
        self.intercept = None

    def __HouseholderTransform(self, A):
        m, n = A.shape
        Q = np.eye(m)
        R = A.copy()

        for j in range(n):
            x = R[j:, j]
            normx = np.linalg.norm(x)
            rho = -np.sign(x[0])
            u1 = x[0] - rho * normx
            u = x / u1
            u[0] = 1
            beta = -rho * u1 / normx

            R[j:, :] = R[j:, :] - beta * np.outer(u, u).dot(R[j:, :])
            Q[:, j:] = Q[:, j:] - beta * Q[:, j:].dot(np.outer(u, u))
        
        return Q, R

    def get_line_from_data(self, data):
        m, n = data.shape
        A = np.array([data[:,0], np.ones(m)]).T
        b = data[:, 1] 

        Q, R = self.__HouseholderTransform(A)
        b_hat = Q.T.dot(b)

        R_upper = R[:n, :]
        b_upper = b_hat[:n]

        slope, intercept = np.linalg.solve(R_upper, b_upper)
        self.slope = slope
        self.intercept = intercept

    def fitting(self, target):
        result = target * self.slope + self.intercept
        return result