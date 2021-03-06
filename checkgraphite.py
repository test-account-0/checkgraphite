#!/usr/bin/env python

import sys
import pynagio
import requests
import pprint
import re
import warnings


def get_data(endpoint, expression, verbose=False, minimum=False,
        last_points_to_ignore=0):
    url = "{}?{}".format(endpoint, expression)
    r = requests.get(url, verify=False)
    raw_data = r.json()
    if verbose:
        print("Raw data from graphite:")
        pprint.pprint(raw_data)
        print("Datapoints:")
    data = {}
    for metric in raw_data:
        key = sanitize_name(metric['target'])
        datapoints = [datapoint[0] for datapoint in metric['datapoints']
                      if datapoint[0]]
        if minimum:
            datapoints = [min(datapoints)]
        if last_points_to_ignore:
            datapoints = datapoints[:-last_points_to_ignore]
        if verbose:
            print(datapoints)
        if len(datapoints) > 0:
            value = float(datapoints[-1])
        else:
            return False
        data[key] = value
    return data


def sanitize_name(string):
    return re.sub('[^a-zA-Z_0-9-]', '_', string)


def main():

    check = pynagio.PynagioCheck()
    check.add_option("--endpoint", "-e",
                     help="Graphite endpoint",
                     dest="endpoint")
    check.add_option("--expression", "-E",
                     help="Graphite expression",
                     dest="expression")
    check.add_option("--verbose", "-v",
                     help="More verbose output",
                     action="store_true")
    check.add_option("--minimum",
                     help="Select minimal value",
                     action="store_true")
    check.add_option("--last-points-to-ignore",
                     help="Number of last points to ignore",
                     dest="last_points_to_ignore",
                     type=int,
                     choices=xrange(0, 1000))
    check.parse_arguments()
    if not check.args.endpoint or not check.args.expression:
        check.parser.error('-e and -E arguments are required')
    endpoint_opt = check.args.endpoint
    expression_opt = check.args.expression

    # ugly hack for urllib3 warnings on older versions of python
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        try:
            data = get_data(endpoint_opt, expression_opt,
                    verbose=check.args.verbose, minimum=check.args.minimum,
                    last_points_to_ignore=check.args.last_points_to_ignore)
        except Exception as e:
            print("Cannot get data")
            print(e)
            sys.exit(1)

    check.add_metrics(data)
    check.exit()

if __name__ == '__main__':
    main()
