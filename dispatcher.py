#!/usr/bin/env python
from pathlib import Path
from slugify import slugify
import json
from collections import namedtuple
import cPickle as pickle


def dispatch(root, tasks, preparer):
    root = Path(root)
    params = [[(k, v[1]) for k, v in t] for t in tasks]
    paths = [root/(('_'.join(slugify(unicode(v)) for k, v in p) or '_') + '.start')
             for p in params]
    tasks = [{k: v[0] for k, v in t} for t in tasks]
    for path, task, param in zip(paths, tasks, params):
        path.mkdir(parents=True)
        preparer(path, task)
        with open(str(path/'info.json'), 'w') as f:
            json.dump(dict(param), f)


Result = namedtuple('Result', ['info', 'data'])


def extract(path, extractor):
    path = Path(path)
    results = []
    for rundir in path.glob('*.done'):
        with open(str(rundir/'info.json')) as f:
            info = json.load(f)
        try:
            data = extractor(rundir/'rundir')
        except:
            print('info: Error occured in {}'.format(rundir))
            raise
        results.append(Result(info, data))
    with (path/'results.p').open('wb') as f:
        pickle.dump(results, f, -1)


def fetch():
    with open('results.p', 'rb') as f:
        return pickle.load(f)
