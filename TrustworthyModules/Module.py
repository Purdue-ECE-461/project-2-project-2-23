import numpy as np
from git import Repo
from git import rmtree
import os

from Util import get_logger

logger = get_logger('Module')
logger.info("Logger init in Module.py")


class Module:
    def __init__(self, name, url, original_url):
        self.name = name                                    # name of repository
        self.repo = None
        self.url = 'https://github.com/' + str(self.name)   # source URL of repo
        self.original_url = original_url
        self.readMe = 0                                     # readMe file contents
        self.open_issues = None                             # array of issues
        self.closed_issues = None                           # array of issues
        self.commits = None                                 # array of commits
        self.stats_contributors = []                        # array of contributors with stats
        self.popularity = 0                                 # score for popularity of the module
        self.weights = []                                   # weight of each score
        self.net_score = 0

        self.correct_class = None
        self.license_class = None
        self.bus_factor_class = None
        self.popularity_class = None
        self.responsiveness_class = None
        self.ramp_up_class = None
        self.dependency_class = None

    def clone_repo(self):
        # Check if the repo already is cloned, if not then clone
        repo = Repo.clone_from(self.url, self.name)  # could maybe use giturl but we dont have that yet
        
    def remove_repo(self):
        # Remove cloned repo
        cwd = os.getcwd()
        directory_folder_empty = os.path.join(cwd, self.name.split("/")[0])
        print(directory_folder_empty)
        rmtree(directory_folder_empty)

    def __str__(self):
        return f"{self.original_url} {round(self.net_score, 1)} {round(self.ramp_up_class.score, 1)} {round(self.correct_class.score, 1)} " \
               f"{round(self.bus_factor_class.score, 1)} {round(self.responsiveness_class.score, 1)} {round(self.dependency_class.score, 1)} " \
               f"{self.license_class.score}"

    def get_weights(self):
        priorities = []
        metric_list = [self.responsiveness_class, self.license_class, self.bus_factor_class, self.ramp_up_class, self.correct_class, self.dependency_class]
        for metric in metric_list:
            priorities.append(metric.priority)
        total = sum(priorities)
        self.weights = [round((priority / total), 2) for priority in priorities]

    def run_score_calculations(self):
        logger.debug("Running metric score calculations")
        self.responsiveness_class.calculate_responsiveness()
        self.correct_class.calculate_score()
        self.bus_factor_class.calculate_score()
        self.license_class.calculate_score()
        self.ramp_up_class.calculate_ramp_up(self.responsiveness_class.score, self.correct_class.score)
        self.dependency_class.calculate_score()

    def calculate_net_score(self):
        # Calculating Net Score with weights
        self.run_score_calculations()

        logger.info(f"Calculating Net Score for {self.name}")
        self.get_weights()
        weights = np.array(self.weights)
        scores = np.array([self.responsiveness_class.score, self.license_class.score,
                           self.bus_factor_class.score, self.ramp_up_class.score,
                           self.correct_class.score, self.dependency_class.score])
        self.net_score = np.round(np.dot(weights, scores), 4)
        return
