import copy

import numpy as np
from scipy.stats import skew

from TrustworthyModules.Metric import Metric
from TrustworthyModules.GithubHelper import last_year_commit_ratio, prev_years_issues_ratio

from TrustworthyModules.Util import get_logger

logger = get_logger('BusFactor')
logger.info("Logger init in BusFactor.py")

# maximum values to normalize against
MAX_STD = 1000
MAX_SKEW = 18
MAX_RESOLVED = 0.8
MAX_RECENT = 0.0075


class BusFactor(Metric):
    # init function for the class.  Submetric weights is hardcoded because easy modification of metric
    # calculations is not a product spec
    def __init__(self, priority, module_name, module_stats_contributors, module_commits):
        super().__init__(priority, module_name)
        self.submetric_weights = {'skew': 0.15, 'std': 0.15, 'recent': 0.1, 'resolved': 0.2, 'high': 0.2, 'total': 0.2}
        self.stats_contributors = \
            module_stats_contributors  # list of contributor type
        self.commits = module_commits  # list of all commits
        self.total_contributors = \
            len(module_stats_contributors) if self.stats_contributors is not None else 0  # all contributors for a repository
        self.contribution_stdev = 0  # standard deviation of number of commits for top 100 contributors in a repo
        self.contribution_skew = 0  # skew of number of commits for top 100 contributors in a repo
        self.recently_resolved = 0  # ratio of resolved issues to all issues in the past year
        self.recent_commits = 0  # ratio of recent commits to total commits
        self.high_contributors = 0  # representative of contributors that have contributed at least half
        # as much as the top contributor

    # normalizes the submetrics based on defined maximum values
    def normalize_scores(self):
        logger.info("Normalizing bus factor scores")

        self.contribution_skew = 1 - min(self.contribution_skew / MAX_SKEW, 1)
        self.contribution_stdev = 1 - min(self.contribution_stdev / MAX_STD, 1)
        self.recently_resolved = min(self.recently_resolved / MAX_RESOLVED, 1)
        self.high_contributors = self.high_contributors
        self.recent_commits = min(self.recent_commits / MAX_RECENT, 1)

        logger.info("Normalized SKEW: " + str(self.contribution_skew))
        logger.info("Normalized STD: " + str(self.contribution_stdev))
        logger.info("Normalized HIGH CONTR.: " + str(self.high_contributors))
        logger.info("Normalized RECENT COMMITS: " + str(self.recent_commits))
        logger.info("Normalized RECENT RESOLVED: " + str(self.recently_resolved))

    def calculate_score(self):
        logger.debug("Calculating total bus factor score")

        if (self.total_contributors == 0):
            self.score = 0
            return

        self.calculate_metrics()
        self.normalize_scores()

        scores = [self.contribution_skew, self.contribution_stdev, self.recently_resolved,
                  self.high_contributors, self.recent_commits, min(self.total_contributors / 75, 1)]

        weights = [self.submetric_weights['skew'], self.submetric_weights['std'], self.submetric_weights['resolved'],
                   self.submetric_weights['high'], self.submetric_weights['recent'], self.submetric_weights['total']]

        self.score = np.round(np.dot(scores, weights), 4)
        if self.score < 0: self.score = 0;

        logger.info("TOTAL Bus Factor Score: " + str(self.score))

    def calculate_metrics(self):
        logger.info("Calculating all the submetrics for bus factor")
        user_information, total_commits = self.generate_array()
        all_contributions = get_contributions(user_information)
        self.high_contributors = calculate_significant_contributors(all_contributions)
        self.recent_commits = last_year_commit_ratio(self.name, self.commits)
        self.recently_resolved = prev_years_issues_ratio(self.name, 1)

        # normalize for no issues; no information -> average:
        if self.recently_resolved == -1:
            self.recently_resolved = MAX_RESOLVED/2

        if self.total_contributors > 6:
            self.contribution_stdev = calculate_std(all_contributions)
            self.contribution_skew = calculate_skew(all_contributions)
        else:
            self.contribution_stdev = MAX_STD
            self.contribution_skew = MAX_SKEW

    # generate a 2D array of stats contributors attributes including name, total commits, and most recent commit
    def generate_array(self):
        user_information_lists = []
        total_contributions = []
        last_weeks = []
        for i in self.stats_contributors:
            user_information_lists.append([i.uid, i.num_commits, i.last_week])
            total_contributions.append(i.num_commits)
            last_weeks.append(i.last_week)

        return user_information_lists, sum(total_contributions)


# gets all contributions in an array from all users (top 100 contributors)
def get_contributions(user_information):
    return np.array(sorted(user_information, key=lambda k: k[1]))[:, 1].astype(float)


# need to pad with zeros to not give smaller projects an advantage
# calculate skew in the number of contributions
def calculate_skew(contributions):
    normalized = list(copy.deepcopy(contributions))
    for i in range(100 - len(contributions)):
        normalized.append(0)
    return skew(normalized)


def calculate_std(contributions):
    normalized = list(copy.deepcopy(contributions))
    for i in range(100 - len(contributions)):
        normalized.append(0)
    return np.std(normalized)


# this is badly named
# calculates number of significant contributors (needs revamping)
def calculate_significant_contributors(contributions_arr):
    contributions = list(contributions_arr)
    max_cont = max(contributions)
    cutoff = max_cont - int(max_cont / 1.16)
    k = 0
    for x in contributions:
        if int(x) >= cutoff:
            k += 1
    return min(1, (k - 1) * 0.25)
