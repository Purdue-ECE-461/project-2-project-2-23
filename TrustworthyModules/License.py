import requests
from Util import get_logger

logger = get_logger('License')
logger.info("Logger init in License.py")


class License:
    def __init__(self, module_path, priority, readMe):
        self.check_all_variables(module_path, priority)
        self.module_path = module_path
        self.priority = priority
        self.score = 0
        self.readMe = readMe

    def calculate_score(self):
        logger.debug("Calculating total License Compatibility score")
        # Public Domain, MIT/X11, BSD-new, LGPLv2.1, LGPLv2.1+
        spdx_id = self.get_spdx_id(self.module_path)
        self.check_variable(spdx_id, "spdx_id")

        calc = self.get_score(spdx_id)
        self.check_variable(calc, "calc")

        logger.debug(f"License score: {calc}")
        self.score = calc

        if self.score == 0:
            self.checkReadMe()

    def get_spdx_id(self, module_path):
        logger.debug(f"License function: get_spdx_id")
        url = "https://api.github.com/repos/" + module_path + "/license"

        response = requests.get(url)
        self.check_variable(response, "Response")

        data = response.json()
        self.check_variable(data, "Data")

        for key, value in data.items():
            if key == "license":
                for key1, value1, in value.items():
                    if key1 == "spdx_id":
                        logger.debug(f"License function: get_spdx_id - {value1}")
                        return value1

        return -1

    def get_score(self, spdx_id):
        logger.debug(f"License function: get_score")
        if spdx_id == -1: return 0

        if spdx_id == "MIT":  return 1
        if spdx_id == "Unlicense": return 1
        if spdx_id == "LGPL-2.1-only": return 1
        if spdx_id == "LGPL-2.1-or-later": return 1
        if spdx_id == "BSD-3-Clause": return 1
        if spdx_id == "X11": return 1

        return 0

    # Error Handling Functions
    def check_variable(self, var, string):
        logger.debug(f"License function: check_variable")
        if var is None:
            print("Correctness: " + string + " is None")
            exit(1)

    def check_all_variables(self, module_path, priority):
        logger.debug(f"License function: check_all_variables")
        self.check_variable(module_path, "Path")
        self.check_variable(priority, "Priority")

    def checkReadMe(self):
        decoded_content = str(self.readMe.decoded_content)
        if 'license' in decoded_content.lower():
            if 'MIT' in decoded_content: self.score = 1
            elif 'Unlicense' in decoded_content: self.score = 1
            elif 'LGPL-2.1-only' in decoded_content: self.score = 1
            elif 'LGPL-2.1-or-later' in decoded_content: self.score = 1
            elif 'BSD-3-Clause' in decoded_content: self.score = 1
            elif 'X11' in decoded_content: self.score = 1
