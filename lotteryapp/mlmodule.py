from lotteryapp.models import *
from user.models import *

# numpy ver 1.19.2
import numpy as np

# current_user = Profile.objects.get(user=request.user.pk)

# 어려운 모델은 AWS에서 사용하기 어려울 것 같아 기본적인 회귀 모델을 사용했습니다.
# 사용 방법은 발주량 데이터와 그 날짜에 Share/Request 여부를 정리한 뒤,
# initialize -> training -> prediction 순으로 사용하면 됩니다.
# class initialize 할 때 파라미터로 item 이름을 넣어주셔야 합니다.
class LogisticRegression:

    def __init__(self, item, author):
        self.name = item
        self.weight = None
        self.intercept = None

    def __forward(self, x):
        z = np.sum(x * self.weight) + self.intercept
        return z

    def __backpropagation(self, x, rms):
        weight_grad = x * rms
        intercept_grad = rms
        return weight_grad, intercept_grad

    def __sigmoid(self, z):
        a = 1 / (1 + np.exp(-z))
        return a

    # x는 발주량 데이터, y는 share/request 여부가 담긴 데이터 입니다.
    def training(self, x, y, epochs=100):
        self.weight = np.ones(x.shape[1])
        self.intercept = 0
        for i in range(epochs):
            for xi, yi in zip(x, y):
                z = self.__forward(xi)
                a = self.__sigmoid(z)
                err = -(yi - a)
                weight_grad, intercept_grad = __self.backpropagation(xi, err)
                self.weight -= weight_grad
                self.intercept -= intercept_grad

    def prediction(self, x):
        z = [self.__forward(xi) for xi in x]
        a = self.__sigmoid(np.array(z))
        # 발주량이 초과 공급인 경우
        if a > 0.6:
            return 1
        # 발주량이 부족한 경우
        elif a < 0.4:
            return -1
        # 발주량이 적정선인 경우
        else:
            return 0