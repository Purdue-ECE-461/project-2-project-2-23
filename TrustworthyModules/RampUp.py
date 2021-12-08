import os
import numpy as np
from git import Repo
from git import rmtree

from TrustworthyModules.Util import get_logger
import TrustworthyModules.GithubHelper as GithubHelper

MAX_README_LENGTH = 5000

logger = get_logger('RampUp')
logger.info("Logger init in RampUp.py")


class RampUp:
    def __init__(self, module_name, url, popularity_score, priority):
        self.module_name = module_name
        self.url = url
        self.readme_length = GithubHelper.get_readme(self.module_name).size
        self.popularity_score = popularity_score
        self.priority = priority

        self.score = 1

    def calculate_ramp_up(self, responsiveness_score, correctness_score):
        logger.info(f"Calculating Ramp Up for {self.module_name}")

        # Weights for each:
        # - 10% ReadMe length
        # - 20% ReadMe examples
        # - 25% Responsiveness and Correctness score
        # - 45% Popularity
        weights = [.1, .2, .25, .45]

        # ReadMe size
        logger.debug(f"Ramp Up: calculating ReadMe length comparison for {self.module_name}")
        score_readme_length = self.readme_length_score_calc()

        # Examples in Repository or ReadMe
        logger.debug(f"Ramp Up: calculating score for repository examples {self.module_name}")
        score_readme_examples = self.readme_examples_score_calc()

        # Use of Responsiveness and Correctness as a way of getting feedback
        logger.debug(f"Ramp Up: calculating score for correctness and responsiveness for {self.module_name}")
        score_responsiveness_correctness = (responsiveness_score + correctness_score) / 2

        # Final Calculation
        logger.debug(f"Ramp Up: calculating final score using popularity score for {self.module_name}")
        self.score = self.final_score_calculation(weights, score_readme_length, score_readme_examples,
                                                  score_responsiveness_correctness)
        if self.score < 0: self.score = 0;
        
        logger.debug(f"Ramp Up: weights calculated {weights}")
        logger.debug(f"Ramp Up: values calculating ramp up {score_readme_length}, {score_readme_examples}, "
                     f"{score_responsiveness_correctness}, {self.popularity_score}")
        logger.debug(f"Ramp Up: final value calculated {self.score}")

        return

    def readme_length_score_calc(self):
        # Compare the repo ReadMe file to an average readme file
        readme_score = self.readme_length / MAX_README_LENGTH
        return readme_score if readme_score <= 1 else 1

    def readme_examples_score_calc(self):
        # Check examples in ReadMe or folder files that help people understand the module
        return self.analyze_readme()

    def final_score_calculation(self, weights, score_readme_length, score_readme_examples,
                                score_responsiveness_correctness):
        # Calculate score depending on the customer weights
        weights = np.array(weights)
        scores = np.array([score_readme_length, score_readme_examples, score_responsiveness_correctness,
                           self.popularity_score])
        return np.round(np.dot(weights, scores), 4)

    def analyze_readme(self):
        # Analyze cloned repository
        score = self.module_clone_readme_analyzer()
        return score

    def module_clone_readme_analyzer(self):
        cwd = os.getcwd()
        directory = os.path.join(cwd, self.module_name)
        is_example_exists = 0
        is_code_in_readme_exists = 0
        for filename in os.listdir(directory):
            # Check if there's an examples folder
            if filename == "examples":
                is_example_exists = 0.3
            # Check if there's code on the ReadMe file
            if filename == "Readme.md" or filename == "README.md" or filename == "ReadMe.md":
                readme_fp = open(os.path.join(directory, filename), 'r')
                readme_content = readme_fp.read()
                if "js" in readme_content or "bash" in readme_content:
                    is_code_in_readme_exists = 0.7
                    # print("There's code")
        return is_code_in_readme_exists + is_example_exists

