#! /usr/bin/env python

import os
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy
from matplotlib import pyplot as plt
from matplotlib import cm

def get_bivariate_normal_and_uniform_densities(maximum = 20.0,
        mean = (2.0, 3.0),
        variance = (0.2, 0.2),
        covariance = 0.0,
        npoints = 50):
    a = numpy.linspace(0, maximum, npoints)
    b = numpy.linspace(0, maximum, npoints)
    X, Y = numpy.meshgrid(a, b)
    Z1 = get_bivariate_normal_density(X, Y,
            mean = mean,
            variance = variance,
            covariance = covariance)
    Z2 = (Z1 * 0.0) + (1.0 / (maximum ** 2))
    return X, Y, Z1, Z2

def get_bivariate_normal_density(x, y,
        mean = (2.0, 3.0),
        variance = (0.2, 0.2),
        covariance = 0.0):
    return matplotlib.mlab.bivariate_normal(x, y,
            sigmax = variance[0],
            sigmay = variance[1],
            mux = mean[0],
            muy = mean[1],
            sigmaxy = covariance)

def get_marginal_likelihood(x, y, z):
    max_x, max_y = 0.0, 0.0
    for i in x:
        max_x = max([max_x] + [max(i)])
    for i in y:
        max_y = max([max_y] + [max(i)])
    prior = 1.0 / (max_x * max_y)
    l = 0.0
    w = 0.0
    for i in range(len(z)):
        for j in range(len(z[0])):
            l += (z[i][j] * prior)
            w += prior
    return l/w

def get_marginal_likelihood_constrained(x, y, z):
    assert len(x) == len(y)
    max_x, max_y = 0.0, 0.0
    for i, a in enumerate(x):
        assert len(x[i]) == len(y[i])
        max_x = max([max_x] + [max(a)])
    for a in y:
        max_y = max([max_y] + [max(a)])
    assert max_x == max_y
    prior = 1.0 / max_x
    l = 0.0
    w = 0.0
    for i in range(len(z)):
        l += (z[i][i] * prior)
        w += prior
    return l/w

def get_marginal_plot(maximum = 20.0,
        mean = (2.0, 3.0),
        variance = (0.2, 0.2),
        covariance = 0.0,
        npoints = 50):
    X, Y, Z1, Z2 = get_bivariate_normal_and_uniform_densities(maximum = maximum,
            mean = mean,
            variance = variance,
            covariance = covariance,
            npoints = npoints)
    ml_2p = get_marginal_likelihood(X, Y, Z1)
    ml_1p = get_marginal_likelihood_constrained(X, Y, Z1)
    sys.stdout.write('marginal likelihood of 2-parameter model: {0}\n'.format(ml_2p))
    sys.stdout.write('marginal likelihood of 1-parameter model: {0}\n'.format(ml_1p))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.plot_surface(X, Y, Z1, rstride=1, cstride=1, linewidth=0.0, antialiased=False, shade=True, cmap=cm.coolwarm, zorder=200)
    a, b, c = [], [], []
    for i in range(len(X)):
        a.append(X[i][i])
        b.append(Y[i][i])
        c.append(Z1[i][i])
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    prior_d = 1.0 / (xmax * ymax)
    prior_d *= 2.0
    x_back_line = ax.plot([xmin, xmax], [ymax, ymax], [prior_d, prior_d])
    x_front_line = ax.plot([xmin, xmax], [ymin, ymin], [prior_d, prior_d], zorder=200)
    y_back_line = ax.plot([xmin, xmin], [ymin, ymax], [prior_d, prior_d], zorder=-10)
    y_front_line = ax.plot([xmax, xmax], [ymin, ymax], [prior_d, prior_d], zorder=200)
    plt.setp([x_back_line, y_back_line, x_front_line, y_front_line],
            color = 'r',
            linestyle = '--',
            linewidth = 1.0,
            marker = '')
    identity_line = ax.plot(a, b, c)
    plt.setp(identity_line,
            color = 'w',
            linestyle = '-',
            linewidth = 0.75,
            marker = '',
            zorder = 100)
    ax.set_xlabel(r'$T_1$', size=14.0)
    ax.set_ylabel(r'$T_2$', size=14.0)
    ax.set_zlabel('Density', size=14.0)
    rect = [-0.12, 0, 1, 1.02]
    fig.tight_layout(pad = 0.25, rect = rect)
    return ax, fig

def main_cli():
    maximum = 1.0
    ax, fig = get_marginal_plot(maximum = maximum,
            mean = (0.15, 0.247),
            variance = (0.039, 0.026),
            covariance=0.0,
            npoints = 100)
    fig.savefig('../images/marginal-plot-3d.pdf')


if __name__ ==  '__main__':
    main_cli()

