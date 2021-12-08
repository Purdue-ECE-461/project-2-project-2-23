from os import path
import TrustworthyModules.Util as Util


# The purpose of this file is to support reading in the URLs and ensure validity

logger = Util.get_logger('IOUtil')
logger.info("Logger init in IOUtil.py")


# verify that the path for the text file is correct
def verify_path(filepath):
    if path.exists(filepath):
        logger.info("path found")
        return filepath
    else: 
        logger.info("path not found")
        return -1


# read in text file to list
def read_input_file(filepath):
    with open(filepath) as f:
        urls = f.read().splitlines() 
    return urls


def output_to_stdout(module):
    first_line = ['URLS', 'NET_SCORE', 'RAMP_UP_SCORE', 'CORRECTNESS_SCORE', 'BUS_FACTOR_SCORE',
                  'RESPONSIVENESS_SCORE', 'DEPENDENCY_SCORE', 'LICENSE_SCORE']

    # Write title line
    print(" ".join(first_line))
    logger.debug(" ".join(first_line))

    # Write module information
    print(str(module))
    logger.debug(str(module))
    return


# This function is to sort the modules in module_list for outputting
def sort_module_list(module_list):
    net_scores_original = []
    sorted_module_list = []
    # Get all the net scores of each module
    for module in module_list:
        net_scores_original.append(float(str(module).split(' ')[1]))
    net_scores_sorted = sorted(net_scores_original, reverse=True)

    # Get the index of the sorted values a put the sorted modules in descending order
    for sorted_score in net_scores_sorted:
        # Get the index of the sorted values
        index_sorted_score_original_list = net_scores_original.index(sorted_score)
        # append the ordered values
        sorted_module_list.append(module_list[index_sorted_score_original_list])
        # Remove the values already in the new sorted module list
        net_scores_original.pop(index_sorted_score_original_list)
        module_list.pop(index_sorted_score_original_list)

    return sorted_module_list
