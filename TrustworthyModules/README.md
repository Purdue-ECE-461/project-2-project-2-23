# Github/npm module ranker (ECE 461)

The system takes in Github or npm URLs and can rank them based on their responsiveness, license compatibility, bus factor, ramp-up time, and correctness. Responsiveness is concerned with how quick issues are handled, as well as response time for other comments. License compatibility is a score that shows if a module’s license is compatible with the desired GNU Lesser General Public License v2.1. Bus factor accounts for how much each contributor does to ensure it is not just one person managing the module. The score for ramp-up time is determined by how quickly a user can learn and use the module by incorporating readMe length, if there are examples, and the issues. Lastly, correctness deals with the ratio of open to closed issues, stale issues, and a lack of updated issues.The end output is a sorted list by net score where each issue has an assumed priority from Sarah’s requirements. In addition, there are tests and logs to ensure success.

## Running Program
How to install dependencies:
./run install

How to run:
./run filename
  <br /> where filename contains npmjs or github URLs for npm packages

How to run tests:
./run test
  <br /> tests are run using the pytest framework

## Adding Metric
