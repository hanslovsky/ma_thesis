#!/usr/bin/python2

import numpy as np
import scipy
import pylab as pl
import matplotlib
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from sklearn import mixture
import vigra

def get_ellipsis(covs, means):
    res = []
    count = 0
    colors = []
    val = 0.7
    for i in range(3):
        color = [0, 0, 0]
        color[i % 3] = val
        colors.append(color)
    for i in range(3):
        color = [val, val, val]
        color[i % 3] = 0
        colors.append(color)

    for cov, mean in zip(covs, means):
        color = colors[count % len(colors)]
        count += 1
        res.append(get_ellipse(cov, mean))
        res[-1].set_color(color)
    return res

def get_ellipse(cov, mean):
    e_vals, e_vecs = scipy.linalg.eig(cov)
    e_vals = 15*e_vals.astype(np.float64)

    angle = np.arccos(e_vecs[0][0])*180/np.pi
    # print angle
    return Ellipse(mean, np.sqrt(e_vals[0]), np.sqrt(e_vals[1]), angle=angle)

def fit_gmm_to_raw(raw, segmentation, n_clusters, linewidth=10, alpha=0.7):
    coords = np.array(np.where(segmentation > 0)).transpose()
    clf = mixture.GMM(n_components=n_clusters, covariance_type='full', n_iter=10000)
    clf.fit(coords)
    ellipsis = get_ellipsis(clf.covars_, clf.means_)
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, raw.shape[0]-1)
    ax.set_ylim(0, raw.shape[1]-1)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    imgplot = plt.imshow(raw.transpose(), cmap = matplotlib.cm.Greys_r)
    for e in ellipsis:
        e.set_alpha(alpha)
        e.set_linewidth(linewidth)
        # e.set_facecolor([1,1,1])
        e.set_fill(False)
        ax.add_artist(e)
    return fig, ax, clf

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', '-r', help='path to raw image', required=True)
    parser.add_argument('--segmentation' ,'-s', help='path to segmentation image', required=True)
    parser.add_argument('--number-of-clusters', '-n', help='number of clusters', required=True, type=int)
    parser.add_argument('--alpha', '-a', type=float, help='opacity', default=0.3)
    parser.add_argument('--linewidth', '-l', type=float, help='linewidth', default=3)
    parser.add_argument('--outfile', '-o', default='')

    args = vars(parser.parse_args())
    raw = np.array(vigra.readImage(args['raw'])[...,0])
    segmentation = np.array(vigra.readImage(args['segmentation'])[...,0])
    fig, ax, clf = fit_gmm_to_raw(raw, segmentation, args['number_of_clusters'], args['linewidth'], args['alpha'])
    pl.gca().invert_yaxis()
    if args['outfile'] == '':
        pl.show()
    else:
        pl.savefig(args['outfile'], bbox_inches='tight', pad_inches=0.0)
    
