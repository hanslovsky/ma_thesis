#!/usr/bin/python2

import numpy as np
import pylab as pl
from sklearn import mixture

n_samples = 3000

# generate random sample, two components
np.random.seed(0)
C_1 = 3.5*np.array([[1.5, 0.45], [0.45, 1.]])
C_2 = 3.5*np.array([[0.8, 0.5], [0.5, 1.7]])
print C_1
print C_2
X_train = np.r_[np.dot(np.random.randn(n_samples, 2), C_1),
                np.dot(np.random.randn(n_samples, 2), C_2) + np.array([15, 15])]
print X_train.shape
X_train = np.r_[np.random.multivariate_normal([0, 0], C_1, n_samples),
                np.random.multivariate_normal([15, 15], C_2, n_samples)]

clf = mixture.GMM(n_components=2, covariance_type='full', n_iter=10000,)


clf.fit(X_train)
print clf.means_
print clf.covars_

x = np.linspace(-10.0, 25.0)
y = np.linspace(-10.0, 25.0)
X, Y = np.meshgrid(x, y)
XX = np.c_[X.ravel(), Y.ravel()]
Z = (clf.score_samples(XX)[0])
# Z = np.log(-clf.score_samples(XX)[0])
# Z = (clf.score(XX))
# Z /= np.max(np.abs(Z))
Z = Z.reshape(X.shape)

fig = pl.figure()
CS = pl.contour(X, Y, Z)
CB = pl.colorbar(CS, shrink=1.0, extend='both')
CC = pl.scatter(X_train[:, 0], X_train[:, 1], .8)
pl.xlabel('x')
pl.ylabel('y')
pl.title("Log Likelihood under the Model")

pl.axis('tight')
pl.show()

