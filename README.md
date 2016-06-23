# checkgraphite
Nagios check for graphite

It is a standard pynagio check.

## Usage:
```
$ ./checkgraphite.py --help
usage: checkgraphite.py [-h] [-t THRESHOLDS [THRESHOLDS ...]]
                        [-T THRESHOLD_REGEXES [THRESHOLD_REGEXES ...]]
                        [--no-perfdata] [-r RATES [RATES ...]]
                        [-R RATE_REGEXES [RATE_REGEXES ...]]
                        [--endpoint ENDPOINT] [--expression EXPRESSION]
                        [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLDS [THRESHOLDS ...]
                        Threshold(s) to check
  -T THRESHOLD_REGEXES [THRESHOLD_REGEXES ...]
                        Threshold regex(es) to check
  --no-perfdata, --np   Threshold regex(es) to check
  -r RATES [RATES ...]  Rates to calculate
  -R RATE_REGEXES [RATE_REGEXES ...]
                        Rates regex to calculate
  --endpoint ENDPOINT, -e ENDPOINT
                        Graphite endpoint
  --expression EXPRESSION, -E EXPRESSION
                        Graphite expression
  --verbose, -v         More verbose output
```


## Example:
```
/checkgraphite.py -e 'https://graphite.example.com/render' -E 'from=-90s&format=json&target=some.graphite.expression.???.pcp.kernel_all_load__1_minute' -t 'metric=some_host_pcp_kernel_all_load__1_minute,warn=2..3,crit=4..inf'
```
