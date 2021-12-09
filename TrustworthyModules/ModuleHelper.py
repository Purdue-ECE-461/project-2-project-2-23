import TrustworthyModules.GithubHelper as GithubHelper
from TrustworthyModules.Users import get_number_users
from TrustworthyModules.Module import Module

logger = GithubHelper.get_logger('ModuleHelper')
logger.info("Logger init in ModuleHelper.py")


def get_attributes(module):
    module.open_issues, module.closed_issues = GithubHelper.get_issues(module.name)
    module.commits = GithubHelper.get_commits(module.name)
    module.contributors = GithubHelper.get_contributors(module.name)
    module.stats_contributors = GithubHelper.get_stats_contributors(module.name)
    module.readMe = GithubHelper.get_readme(module.name)
