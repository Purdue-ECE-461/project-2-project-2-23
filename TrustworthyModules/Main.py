import copy
import datetime
import sys
import numpy as np
import os

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

logger = get_logger('Main')
logger.info("Logger init in Main.py")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def run_rank_mode(url):
    blockPrint()
    begin_time = datetime.datetime.now()
    logger.info("This will be fun!")

    logger.info("Running Rank Mode!")
    if url != '':
        logger.info("Getting the repository path")
        repo_path, module = get_repo_path(url)
        logger.debug("Repository Path:")
        logger.debug(str(repo_path))

        # Get attributes for the model
        logger.info(f"Getting repo attributes for {module.name}")
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
        logger.info(f"Calculating metrics for {module.name}")
        module.clone_repo()
        module.calculate_net_score()
        module.remove_repo()

        ret_scores = {'NET_SCORE':module.net_score, 'RAMP_UP_SCORE':module.ramp_up_class.score, \
            'CORRECTNESS_SCORE':module.correct_class.score, 'BUS_FACTOR_SCORE':module.bus_factor_class.score, \
                'RESPONSIVENESS_SCORE':module.responsiveness_class.score, 'DEPENDENCY_SCORE':module.dependency_class.score, \
                    'LICENSE_SCORE':module.license_class.score}

        #logger.info("Output module values with their metrics")
        IOUtil.output_to_stdout(module)

        logger.info(f"Time running the code: {datetime.datetime.now() - begin_time}")
        logger.info("This fun is done")

        enablePrint()
        return ret_scores
    else:
        enablePrint()
        print("Non-Existent URL Given as Input")
        exit(1)


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    logger.info("This will be fun!")

    if sys.argv[1] == "rank_mode":
        _ = run_rank_mode(sys.argv[2])

    logger.info(f"Time running the code: {datetime.datetime.now() - begin_time}")
    logger.info("This fun is done")