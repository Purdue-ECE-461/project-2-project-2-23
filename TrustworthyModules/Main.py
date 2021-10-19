import copy
import datetime
import sys

import IOUtil
from GithubHelper import get_repo_paths
from ModuleHelper import get_attributes
from Util import *
from Correctness import Correctness
from License import License
from BusFactor import BusFactor
from Popularity import Popularity
from Responsiveness import Responsiveness
from RampUp import RampUp

logger = get_logger('Main')
logger.info("Logger init in Main.py")


def run_rank_mode(path):
    logger.info("Running Rank Mode!")
    if IOUtil.verify_path(path) != -1:
        logger.info("Reading input file and getting the repository paths")
        urls = IOUtil.read_input_file(path)
        repo_paths, module_list = get_repo_paths(urls)
        logger.debug("Repository Paths:")
        logger.debug(str(repo_paths))

        # Get attributes for each model
        for module in module_list:
            logger.info(f"Getting repo attributes for {module.name}")
            get_attributes(module)
            module.popularity_class = Popularity(module.name, module.url)
            module.popularity = module.popularity_class.calculate_popularity()
            module.correct_class = Correctness(module.name, module.open_issues, module.closed_issues, 2,
                                               module.popularity)
            module.license_class = License(module.name, 5, module.readMe)
            module.bus_factor_class = BusFactor(4, module.name, module.stats_contributors, module.commits)
            module.responsiveness_class = Responsiveness(module.name, module.url, module.open_issues,
                                                         module.closed_issues, 7)
            module.ramp_up_class = RampUp(module.name, module.url, module.popularity, 2)

        # Calculate Metrics for each model
        ret_val = []
        for module in module_list:
            logger.info(f"Calculating metrics for {module.name}")
            module.calculate_net_score()
            ret_val.append(module.net_score)


        logger.info("Output module values with their metrics")
        IOUtil.output_to_stdout(module_list)

        return ret_val
    else:
        print("Non-Existent File Given as Input")
        exit(1)


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    logger.info("This will be fun!")

    if sys.argv[1] == "rank_mode":
        _ = run_rank_mode(sys.argv[2])

    logger.info(f"Time running the code: {datetime.datetime.now() - begin_time}")
    logger.info("This fun is done")
