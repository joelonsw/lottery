from lotteryapp.models import *
from user.models import *

# numpy ver 1.19.2
import numpy as np

# Linear regression을 이용한 예측 모델입니다.
# Householder 변환을 이용했습니다. (자세한 알고리즘은 구글링)
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

    # utils.py에 있는 calibrate_RS_data 함수를 통해 정리된 데이터로 학습합니다.
    # parameter로 위 함수의 return 배열이 필요합니다.
    # 학습이 완료되면 slope와 intercept를 저장합니다.
    def get_line_from_data(self, data):
        if len(data) == 0:
            return
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

    # 모델 학습을 완료시킨 후, target parameter에 값을 넣으면 예측 값을 반환합니다.
    def fitting(self, target):
        result = target * self.slope + self.intercept
        return result