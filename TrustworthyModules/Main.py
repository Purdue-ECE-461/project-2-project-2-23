import copy
import datetime
import sys
import numpy as np
import os
from queue import Queue

import TrustworthyModules.IOUtil as IOUtil
from TrustworthyModules.GithubHelper import get_repo_path
from TrustworthyModules.ModuleHelper import get_attributes
from TrustworthyModules.Correctness import Correctness
from TrustworthyModules.License import License
from TrustworthyModules.BusFactor import BusFactor
from TrustworthyModules.Popularity import Popularity
from TrustworthyModules.Responsiveness import Responsiveness
from TrustworthyModules.RampUp import RampUp
from TrustworthyModules.Dependency import Dependency
from TrustworthyModules.Util import get_logger
from TrustworthyModules.base64_helper import base64_helper

logger = get_logger('Main')
logger.info("Logger init in Main.py")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def run_rank_mode(url, q):
    logger.info("-------------Running Trustworthy Modules-------------")
    logger.info("-----------------------------------------------------")

    blockPrint()
    begin_time = datetime.datetime.now()
    scores = {}

    if url != '':
        logger.info("Getting repository path...")
        repo_path, module = get_repo_path(url)
        logger.debug("Repository Path:")
        logger.debug(str(repo_path))

        # Get attributes for the model
        logger.info(f"Getting repo attributes for {module.name}...")
        get_attributes(module)
        module.popularity_class = Popularity(module.name, module.url)
        module.popularity = module.popularity_class.calculate_popularity()
        module.correct_class = Correctness(module.name, module.open_issues, module.closed_issues, 2, module.popularity)
        module.license_class = License(module.name, 5, module.readMe)
        module.bus_factor_class = BusFactor(4, module.name, module.stats_contributors, module.commits)
        module.responsiveness_class = Responsiveness(module.name, module.url, module.open_issues, module.closed_issues, 7)
        module.ramp_up_class = RampUp(module.name, module.url, module.popularity, 2)
        module.dependency_class = Dependency(module.name, module.url, 4)

        # Calculate Metrics for each model
        logger.info(f"Calculating metrics for {module.name}...")
        module.clone_repo()
        module.calculate_net_score()
        base64_encoded = base64_helper('tmp/' + module.name)
        module.remove_repo()

        scores = {'NET_SCORE':module.net_score, 'RAMP_UP_SCORE':module.ramp_up_class.score, \
            'CORRECTNESS_SCORE':module.correct_class.score, 'BUS_FACTOR_SCORE':module.bus_factor_class.score, \
                'RESPONSIVENESS_SCORE':module.responsiveness_class.score, 'DEPENDENCY_SCORE':module.dependency_class.score, \
                    'LICENSE_SCORE':module.license_class.score}

        logger.debug(str(scores))

        logger.info(f"Time running the code: {datetime.datetime.now() - begin_time}")
        logger.info("This fun is done")

        enablePrint()
        retvals = base64_encoded, scores
    else:
        enablePrint()
        logger.error("Non-Existent URL Given as Input")
        retvals = '', []

    logger.info("-----------------------------------------------------")
    logger.info("-----------------------------------------------------")

    if retvals[0] is None or retvals[1] is None:
        exit(1)
    else: q.put(retvals) # originally just returned retvals


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    logger.info("This will be fun!")

    if sys.argv[1] == "rank_mode":
        _ = run_rank_mode(sys.argv[2])

    logger.info(f"Time running the code: {datetime.datetime.now() - begin_time}")
    logger.info("This fun is done")