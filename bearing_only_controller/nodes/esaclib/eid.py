import numpy as np
from numpy import exp, sqrt, pi, cos, sin
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
from scipy import interpolate
from odeint2 import monte_carlo
import time
def rot(theta):
    return np.array([[cos(theta), -sin(theta)],[sin(theta), cos(theta)]])

class EID:

    def __init__(self):

        self.ndiv = 10.0
        self.param_space = np.meshgrid(np.arange(0,1,1./self.ndiv),
                        np.arange(0,1,1./self.ndiv))
        self.state_space = np.meshgrid(np.arange(0,1,1./self.ndiv),
                        np.arange(0,1,1./self.ndiv))
        # self.state_space[0] = self.state_space[0].ravel()
        # self.state_space[1] = self.state_space[1].ravel()
        self.param_lim = [[0,1],[0,1]]
        self.x_lim = [[0,1],[0,1]]
        self.n = 100
        self.psamp = [np.random.uniform(low=i[0], high=i[1], size=self.n) for i in self.param_lim]
    def _fim(self, x, y, xc, yc):

        hdx = self.hdx(np.array([x,y]), np.array([xc, yc]))
        fim = hdx.dot(self.inv_cov).dot(hdx.T)

        return fim

    def _eim(self, x, y):
        # integrand = map(lambda xc, yc: self._fim(x,y,xc,yc)*self.belief.pdf(np.c_[xc,yc]), self.psamp[0], self.psamp[1])
        integrand = map(lambda xc, yc: self._fim(x,y,xc,yc)*self.belief.pdf([xc,yc]), self.psamp[0], self.psamp[1])
        eim = np.sum(integrand, axis=0)/float(self.n)
        return eim

    def _eid(self):
        self.inv_cov = np.linalg.inv(self.cov) # do this now to prevent calculating the inverse later
        # xsamp = [np.random.uniform(low=i[0], high=i[1], size=self.n) for i in self.x_lim]
        self.psamp = [np.random.uniform(low=i[0], high=i[1], size=self.n) for i in self.param_lim]

        # start = time.time()
        eim = map(self._eim, self.state_space[0].ravel(), self.state_space[1].ravel())
        # end = time.time()
        # print 'EIM: ', end-start

        # start = time.time()
        eid = map(np.linalg.det, eim)
        # end = time.time()
        # print 'EID: ', end-start
        # normalize
        eid /= np.sum(eid)/float(self.n)
        # self.eid = eid
        self.eid = eid.reshape(self.state_space[0].shape)
        # plt.imshow(self.eid, extent=(0,1,0,1), origin='lower')
        # plt.colorbar()
        # plt.show()
