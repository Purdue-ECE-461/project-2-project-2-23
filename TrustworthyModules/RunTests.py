import coverage
# Start the code coverage detection
tot_coverage = coverage.coverage()
tot_coverage.start()

import pytest
import json
from test_general import call_tests
import sys
import os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    blockPrint()
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
    tot_coverage.html_report()
    tot_coverage.stop()
    enablePrint()
    print("Total: {}".format(total_tests))
    print("Passed: {}".format(total_passed))
    print("Coverage: {:.2f}%".format(cov))

    print("{}/{} test cases passed. {:.2f}% line coverage acheived".format(total_passed, total_tests, cov))
