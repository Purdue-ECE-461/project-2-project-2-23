import coverage
# Start the code coverage detection
tot_coverage = coverage.coverage() #pragma: no cover
tot_coverage.start() #pragma: no cover

import pytest #pragma: no cover
import json #pragma: no cover
from TrustworthyModules.test_general import call_tests #pragma: no cover
import sys #pragma: no cover
import os #pragma: no cover

# Disable
def blockPrint(): #pragma: no cover
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint(): #pragma: no cover
    sys.stdout = sys.__stdout__


def runtests(): #pragma: no cover
    #blockPrint()
    total_passed, total_tests = call_tests()
    
    '''# read in json file 1 test_report.json
    test_file = open('.report.json',)
    test_coverage = open('coverage.json',)
    test_data = json.load(test_file)
    cov_data = json.load(test_coverage)
    test_file.close()
    test_coverage.close()
    
    total_tests = test_data['summary']['total']

    if 'passed' in test_data['summary']:
        total_passed = test_data['summary']['passed']
    else:
        total_passed = 0

    coverage = cov_data['totals']['percent_covered']'''

    cov = tot_coverage.report()
    tot_coverage.stop()
    enablePrint()
    print("Total: {}".format(total_tests))
    print("Passed: {}".format(total_passed))
    print("Coverage: {:.2f}%".format(cov))

    print("{}/{} test cases passed. {:.2f}% line coverage acheived".format(total_passed, total_tests, cov))
