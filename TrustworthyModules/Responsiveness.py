import datetime

from Util import get_logger

logger = get_logger('Responsiveness')
logger.info("Logger init in Responsiveness.py")


class Responsiveness:
    def __init__(self, module_name, url, open_issues, closed_issues, priority):
        self.module_name = module_name
        self.url = url
        self.open_issues = open_issues
        self.num_open_issues = open_issues.totalCount
        self.closed_issues = closed_issues
        self.num_closed_issues = closed_issues.totalCount
        self.today_date = datetime.datetime.now()
        self.ratio_open_closed_issues = 0
        self.score = 1
        self.priority = priority

    def calculate_responsiveness(self):
        logger.info(f"Calculating Responsiveness for {self.module_name}")
        # Total issues calculated
        if self.num_open_issues > 0 or self.num_closed_issues > 10:
            logger.debug(f"Responsiveness: calculating issues ratio for {self.module_name}")
            self.ratio_open_closed_issues = self.calculating_total_issues()
            self.score -= self.ratio_open_closed_issues
            # Open issues
            logger.debug(f"Responsiveness: calculating open issues analysis for {self.module_name}")
            self.score -= self.calculating_open_issues_deductions()
            # Closed issues
            logger.debug(f"Responsiveness: calculating closed issues analysis for {self.module_name}")
            self.score -= self.calculating_closed_issues_deductions()
            self.score = round(self.score, 4)
            logger.debug(f"Responsiveness: final score calculated {self.score}")
        else:
            self.score = 0.5
        return

    def calculating_total_issues(self):
        if self.num_open_issues + self.num_closed_issues == 0:
            ratio_open_closed_issues = 0
        else:
            ratio_open_closed_issues = round(self.num_open_issues / (self.num_open_issues + self.num_closed_issues), 5)
        return ratio_open_closed_issues

    def calculating_open_issues_deductions(self):
        deduction = 0
        # We will check if the open issues have been open for too long (1 year) and make deductions
        # if that occurs in an issues
        for issue in self.open_issues:
            open_issue_days_passed = str(self.today_date - issue.created_at)
            if "days" in open_issue_days_passed:
                open_issue_days_passed = open_issue_days_passed.split(' ')[0]
                num_days_limit = 365  # Deduct %1 if n days have passed, n = 180 days = ~6 months
                is_percentage_deducted_open = int(open_issue_days_passed) // num_days_limit  # Floor division
                deduction = self.deduction_comments_check(issue, is_percentage_deducted_open,
                                                          deduction)
        return deduction

    def calculating_closed_issues_deductions(self):
        deduction = 0
        # We will check if the closed issues were open for too long (1.5 year) and make deductions
        # if that occurs in an issues
        for issue in self.closed_issues:
            closed_issue_days_passed_open = str(issue.closed_at - issue.created_at)
            if "days" in closed_issue_days_passed_open:
                closed_issue_days_passed_open = closed_issue_days_passed_open.split(' ')[0]
                num_days_limit = 546  # Deduct %1 if n days have passed, n = 365 days
                is_percentage_deducted_closed = int(closed_issue_days_passed_open) // num_days_limit  # Floor division
                deduction = self.deduction_comments_check(issue, is_percentage_deducted_closed,
                                                          deduction)
        return deduction

    def deduction_comments_check(self, issue, is_percentage_deducted, deduction):
        # If it passed more than n days open and less than 3 comments, then deduct points to its responsiveness
        if is_percentage_deducted > 0 and issue.comments < 3:
            deduction += round((0.01 * self.ratio_open_closed_issues), 4)
        return deduction
