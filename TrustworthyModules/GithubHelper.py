import re
import datetime
from pprint import pprint
import requests
from github import Github
from TrustworthyModules.Module import Module
from TrustworthyModules.Util import get_logger
from TrustworthyModules.Contributor import Contributor
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

logger = get_logger('GithubHelper')
logger.info("Logger init in GithubHelper.py")

# Get path to repository from url
def get_repo_path(url):
    repo_path = ''
    module = ''
    if "https://github.com" in url:
        repo_path = get_path(url)
        module = Module(repo_path, url, url)
    elif "https://www.npmjs.com" in url:
        package = url.rsplit('/', 1)[-1]
        github_url = url_from_npm(package)
        repo_path = get_path(github_url)
        module = Module(repo_path, github_url, url)
    else:
        logger.error("INVALID URL")
    return repo_path, module


# Get path to repository from url
def get_path(url):
    return re.search(r"github\.com\/([\w\/-]*)", url).group(1)


# Get path to repository from url
'''def get_repo_paths(urls):
    repo_paths = []
    module_list = []
    for url in urls:
        if "https://github.com" in url:
            path = get_repo_path(url)
            repo_paths.append(path)
            m = Module(path, url, url)
            module_list.append(m)
        elif "https://www.npmjs.com" in url:
            package = url.rsplit('/', 1)[-1]
            github_url = url_from_npm(package)
            path = get_repo_path(github_url)
            repo_paths.append(path)
            m = Module(path, github_url, url)
            module_list.append(m)
        else:
            logger.error("INVALID URL")
    return repo_paths, module_list'''


# Get Github URL from NPM URL
def url_from_npm(package):
    git_url = ""
    base_url = "https://replicate.npmjs.com/"
    npm_url = base_url + package
    r = requests.get(npm_url)
    repo_info = r.json()["repository"]
    if repo_info["type"] == "git":
        git_url = repo_info["url"]
    return git_url


# Get and print issues for a repository
# can be used for: ramp-up, correctness, responsiveness
def get_issues(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    open_issues = repo.get_issues(state="open")
    closed_issues = repo.get_issues(state="closed")
    return open_issues, closed_issues


# Get and print issues for a repository
# can be used for: ramp-up, correctness, responsiveness
def get_issues_since(repo_path, since_date):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    open_issues = repo.get_issues(state="open", since=since_date)
    closed_issues = repo.get_issues(state="closed", since=since_date)
    return open_issues, closed_issues


# Returns ReadMe content variable
# can be used for: ramp-up
def get_readme(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    readme = repo.get_readme()
    return readme


# Returns PaginatedList of NamedUsesr
# May throw exception when accessing variable attributes: Must have push access to view repository collaborators.\
# could probably delete, stick with contributors
# can be used for: bus factor, responsiveness?
''' def get_collaborators(repo_path):
    repo = g.get_repo(repo_path)
    collaborators = repo.get_collaborators()
    return collaborators'''


# Returns PaginatedList of NamedUser
# can get totalCount without exception
# can be used for: bus factor, responsiveness?
def get_contributors(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    contributors = repo.get_contributors()
    return contributors


# Returns list of StatsContributor
# can be used for: bus factor
# StatsContributor Object has : author, total, week
def get_stats_contributors(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    stats_contributors = repo.get_stats_contributors()

    contributors = []
    if stats_contributors is not None:
        for contributor in stats_contributors:
            c = Contributor(contributor.author.name, contributor.total, contributor.weeks, contributor.author.node_id)
            contributors.append(c)

    return contributors


# Returns PaginatedList of Commit
# can be used for: bus factor?, responsiveness,
def get_commits(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    commits = repo.get_commits()
    return commits


def get_commits_since(repo_path, date):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    commits_since = repo.get_commits(since=date)
    return commits_since


# Returns PaginatedList of Commit
# can be used for: bus factor?, responsiveness,
def get_commits_time(repo_path, start_time, end_time):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    commits = repo.get_commits(since=start_time, until=end_time)
    return commits


# Returns PaginatedList of Commit
# can be used for: bus factor?, responsiveness,
''' def get_commits_time_author(repo_path, start_time, end_time, author):
    repo = g.get_repo(repo_path)
    commits = repo.get_commits(since=start_time, until=end_time, author=author)
    return commits '''


# Returns list of Clones
# can be used to determine popularity
# can be used for: ramp-up, correctness, responsiveness?
# need push access to print clones
''' def get_clones(repo_path):
    repo = g.get_repo(repo_path)
    clones = repo.get_clones_traffic()
    return clones '''


# Returns PaginatedList of Download
# can be used to determine popularity
# can be used for: ramp-up, correctness, responsiveness?
# test has totalCount = 0 for all....?
''' def get_downloads(repo_path):
    repo = g.get_repo(repo_path)
    downloads = repo.get_downloads()
    return downloads'''


# Returns PaginatedList of NamedUser
# can be used to determine popularity
# can be used for: ramp-up, correctness, responsiveness?
# totalCount looks to cap at 40,000....?
def get_stargazers(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    stargazers = repo.get_stargazers()
    return stargazers


# Returns PaginatedList of NamedUser
# can be used to determine popularity
# can be used for: ramp-up, correctness, responsiveness?
def get_subscribers(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    subscribers = repo.get_subscribers()
    return subscribers


# Returns list of StatsCommitActivity
# can be used for: bus factor?, responsiveness
def get_stats_commit_activity(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    stats_commit_activity = repo.get_stats_commit_activity()
    return stats_commit_activity


# Returns a PaginatedList of NamedUser
# can be used to determine popularity
# can be used for: ramp-up, correctness, responsiveness?
# same as stargazers
def get_watchers(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    watchers = repo.get_watchers()
    return watchers


# Returns a ContentFile
# can be used for: license compat
# need push access
'''def get_license(repo_path):
    repo = g.get_repo(repo_path)
    license = repo.get_clones_traffic()
    return license'''


# Returns a PaginatedList
# can be used to determine popularity
# can be used for: ramp-up, correctness, responsiveness?
def get_forks(repo_path):
    repo = g.get_repo(repo_path) #@@@@@@@@@@@@@@
    forks = repo.get_forks()
    return forks


'''def get_releases(repo_path):
    repo = g.get_repo(repo_path)
    releases = repo.get_releases()
    return releases'''


# can add get_stats_participation(), get_workflow() too if we feel necessary

# pass in repo path and number of years
# return the ratio of open issues to all issues in that time frame
# returns -1 if there are no issues
def prev_years_issues_ratio(repo_path, years):
    year_ago = datetime.datetime.now() - datetime.timedelta(days=(365 * years))
    open_issues, closed_issues = get_issues_since(repo_path, year_ago)
    total_issues = open_issues.totalCount + closed_issues.totalCount
    if total_issues > 0:
        ret_val = 1 - (open_issues.totalCount / total_issues)
    else:
        ret_val = -1
    return ret_val


# returns the number of commits in the last year
''' def prev_years_commits(repo_path, total_commits, years):
    commits = get_commits_time(repo_path, datetime.datetime.now() - datetime.timedelta(days=(365 * years)),
                               datetime.datetime.now())
    all_commits = total_commits.totalCount
    lasts = commits.totalCount
    ratio = lasts / all_commits
    return ratio '''


# returns ratio of commits in the last year to all time
def last_year_commit_ratio(repo_path, total_commits):
    commits = get_commits_time(repo_path, datetime.datetime.now() - datetime.timedelta(days=365),
                               datetime.datetime.now())
    all_commits = total_commits.totalCount
    last_year = commits.totalCount
    ratio = last_year / all_commits
    return ratio
