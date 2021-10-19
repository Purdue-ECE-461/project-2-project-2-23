import datetime
import GithubHelper
import numpy
from Util import get_logger

logger = get_logger('Correctness')
logger.info("Logger init in Correctness.py")


class Correctness:
    def __init__(self, path, open_issues, closed_issues, priority, popularity):
        self.check_all_variables(path, open_issues, closed_issues, priority, popularity)
        self.module_path = path
        self.open_issues = open_issues
        self.closed_issues = closed_issues
        self.weights = [.75, .25]
        self.priority = priority
        self.popularity = popularity
        self.score = 0

    def calculate_score(self):
        logger.info(f"Calculating Correctness for {self.module_path}")
        if self.open_issues.totalCount == 0 & self.closed_issues.totalCount == 0:
            self.score = .5
        else:
            # issues, + not updated, + stale
            bad_updated = self.bad_updated_count()
            old_issues = self.year_old_count()
            inner = (self.closed_issues.totalCount - bad_updated - old_issues) / (
                    self.closed_issues.totalCount + self.open_issues.totalCount)

            self.check_sizes([inner, self.popularity], self.weights)
            final = numpy.dot([inner, self.popularity], self.weights)

            # lack of commits since most recent issue
            date, most_recent = self.get_most_recent_issue()
            self.check_variable(date, "Date")
            self.check_variable(most_recent, "Most_recent")

            desired_commits = self.get_commits_since(date)
            self.check_variable(desired_commits, "Desired_commits")

            deduction = self.determine_deduction(most_recent, desired_commits.totalCount)
            self.check_variable(deduction, "Deduction")

            self.score = round(final * (1 - deduction), 4)

    def bad_updated_count(self):
        logger.debug(f"Correctness function: bad_updated_count")
        count = 0
        today_date = datetime.datetime.now()
        self.check_variable(today_date, "Today_date (bad_updated_count)")

        for issue in self.open_issues:
            updated_days = (today_date - issue.updated_at)
            if issue.created_at == issue.updated_at:
                count += 1
            elif updated_days.days >= (365/2):
                count += 1

        logger.debug(f"Correctness function: bad_updated_count - {count} issues not updated in last 6 months")
        return count

    def year_old_count(self):
        logger.debug(f"Correctness function: year_old_count")
        count = 0
        today_date = datetime.datetime.now()
        self.check_variable(today_date, "Today_date (year_old_count)")

        for issue in self.open_issues:
            open_issue_days_passed = (today_date - issue.created_at)
            if open_issue_days_passed.days >= 365:
                count += 1

        logger.debug(f"Correctness function: year_old_count - {count} open issues at least a year old")
        return count

    def get_most_recent_issue(self):
        logger.debug(f"Correctness function: get_most_recent_issue")
        most_recent = 999999999
        today_date = datetime.datetime.now()
        self.check_variable(today_date, "Today_date (get_most_recent_issue)")

        updated_date = datetime.datetime.now()
        self.check_variable(today_date, "Updated_date (get_most_recent_issue)")

        for issue in self.open_issues:
            updated_issue_days_passed = (today_date - issue.created_at)
            if updated_issue_days_passed.days < most_recent:
                most_recent = updated_issue_days_passed.days
                updated_date = issue.updated_at

        logger.debug(f"Correctness function: get_most_recent_issue - {most_recent} days since last issue")
        return updated_date, most_recent

    def get_commits_since(self, date):
        logger.debug(f"Correctness function: get_commits_since")

        desired_commits = GithubHelper.get_commits_since(self.module_path,date)

        logger.debug(f"Correctness function: get_commits_since - {desired_commits.totalCount} commits")
        return desired_commits

    def determine_deduction(self, days, commits):
        logger.debug(f"Correctness function: determine_deduction")
        month = self.determine_month(days)
        if month == 0:
            logger.debug(f"Correctness function: determine_deduction - 0 deduction")
            return 0
        elif commits/month > 1:
            logger.debug(f"Correctness function: determine_deduction - 0 deduction")
            return 0
        else:
            logger.debug(f"Correctness function: determine_deduction - {(1/12)*month} deduction")
            return (1/12)*month

    def determine_month(self, days):
        logger.debug(f"Correctness function: determine_month")
        month = 0
        if days < 30:
            month = 0
        elif days < 60:
            month = 1
        elif days < 90:
            month = 2
        elif days < 120:
            month = 3
        elif days < 150:
            month = 4
        elif days < 180:
            month = 5
        elif days < 210:
            month = 6
        elif days < 240:
            month = 7
        elif days < 270:
            month = 8
        elif days < 300:
            month = 9
        elif days < 330:
            month = 10
        elif days < 360:
            month = 11
        else:
            month = 12

        return month

    # Error Handling Functions
    def check_variable(self, var, string):
        logger.debug(f"Correctness function: check_variable")
        if var is None:
            print("Correctness: " + string + " is None")
            exit(1)

    def check_all_variables(self, path, open_issues, closed_issues, priority, popularity):
        logger.debug(f"Correctness function: check_all_variables")
        self.check_variable(path, "Path")
        self.check_variable(open_issues, "Open Issues")
        self.check_variable(closed_issues, "Closed Issues")
        self.check_variable(priority, "Priority")
        self.check_variable(popularity, "Popularity")

    def check_sizes(self, list, weights):
        if len(list) != len(weights):
            print("Correctness: different sizes")
            exit(1)