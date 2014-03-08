#!/usr/bin/python2

import vigra
import h5py
import numpy as np
from collections import defaultdict


def get_bounding_box(oid, features):
    xmin, ymin = features['Coord<Minimum> '][oid]
    xmax, ymax = features['Coord<Maximum> '][oid]
    return ((xmin, ymin), (xmax, ymax))

def fill_dict(object_string):
    res = defaultdict(list)
    for pair in object_string.split(';'):
        (ts, oid) = pair.split(',')
        res[ts].append(int(oid))
    return res

def cut_out(raw, label, bb):
    slicing = (slice(bb[0][0], bb[1][0]+1), slice(bb[0][1], bb[1][1]+1))
    return raw[slicing], label[slicing]

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--objects', '-o', required=True)
    parser.add_argument('--raw', '-r', required=True)
    parser.add_argument('--label', '-l', required=True)
    args = vars(parser.parse_args())
    objects = fill_dict(args['objects'])
    print objects
    with h5py.File(args['raw'], 'r') as raw_file:
        with h5py.File(args['label'], 'r') as label_file:
            for ts, oids in objects.iteritems():
                print "processing timestep %s" % ts
                sel_str = 'ObjectExtraction/LabelImage/0/[[%s, 0, 0, 0, 0], [%s, 1344, 1024, 1, 1]]' % (ts, str(int(ts)+1))
                label = label_file[sel_str][...].squeeze()
                raw = raw_file['volume/data'][int(ts),...].squeeze().astype(np.uint8)
                features = vigra.analysis.extractRegionFeatures(label.astype(np.float32), label, features='all')
                for oid in oids:
                    bb = get_bounding_box(oid, features)
                    raw_cut, label_cut = cut_out(raw, label, bb)
                    fn_base = 't=%s,id=%d' % (ts, oid) 
                    fn_raw = fn_base + '_raw.png'
                    fn_label = fn_base + '_label.png'
                    indices = label_cut == oid
                    raw_cut[np.invert(indices)] = 0
                    vigra.impex.writeImage(raw_cut, fn_raw)
                    vigra.impex.writeImage(255*(indices), fn_label)
