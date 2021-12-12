import datetime
import pytest
import sys
import os

from TrustworthyModules.Module import Module
import TrustworthyModules.Main as Main
import TrustworthyModules.IOUtil as IOUtil
import TrustworthyModules.GithubHelper as GithubHelper
from TrustworthyModules.Users import get_number_users
from TrustworthyModules.Contributor import Contributor
from TrustworthyModules.Correctness import Correctness
from TrustworthyModules.License import License
from TrustworthyModules.BusFactor import BusFactor, calculate_std
from TrustworthyModules.Popularity import Popularity
from TrustworthyModules.Responsiveness import Responsiveness
from TrustworthyModules.RampUp import RampUp
from TrustworthyModules.Dependency import Dependency


# end to end test of low performing repo
def test_end_to_end_even():
    _, module_dict = Main.run_rank_mode('https://github.com/jonschlinkert/even')
    if module_dict['NET_SCORE'] < 0.8: return 1
    else: return 0


# end to end test of high performing repo
def test_end_to_end_jquery():
    _, module_dict = Main.run_rank_mode('https://www.npmjs.com/package/browserify')
    if module_dict['NET_SCORE'] > 0.4: return 1
    else: return 0


# check that an invalid path is caught
def test_verify_path():
    if IOUtil.verify_path("xxd") == -1: return 1
    else: return 0


# check that input files are read properly
'''def test_read_input():
    if IOUtil.read_input_file('test_files/test_file') == ["https://github.com/jquery/jquery"]: return 1
    else: return 0'''


# validate standard deviation calculation in BusFactor
def test_calculate_std():
    if calculate_std([1, 1, 1, 1]) - 0.195959 < 0.001: return 1
    else: return 0


# test that correct number of total contributors is obtained in BusFactor creation
def test_total_contributors():
    sample_mod = Module('jonschlinkert/even', 'https://github.com/jonschlinkert/even', 'https://github.com/jonschlinkert/even')
    sample_mod.stats_contributors = GithubHelper.get_stats_contributors('jonschlinkert/even')
    wks = sample_mod.stats_contributors[0].weeks

    c1 = Contributor('me', 90, wks, '1')
    c2 = Contributor('me', 90, wks, '1')
    c3 = Contributor('me', 89, wks, '1')

    busObj = BusFactor(7, 'test', [c1, c2, c3], None)

    total_cont = busObj.total_contributors

    if total_cont == 3: return 1
    else: return 0


# test that the correct number of commits is fetched
def test_get_commits():
    commits = GithubHelper.get_commits('jonschlinkert/eval-estree-expression')
    count = commits.totalCount
    if count >= 32: return 1
    else: return 0


# test that the correct commit ratio for the past year is calculated
def test_get_year_commit_ratio():
    if datetime.date.today() > datetime.date(2022, 7, 18):
        pytest.skip("Past a year from initial commit; cannot ensure test validity")

    commits = GithubHelper.get_commits('jonschlinkert/eval-estree-expression')
    ratio = GithubHelper.last_year_commit_ratio('jonschlinkert/eval-estree-expression', commits)
    if ratio == 1.0: return 1
    else: return 0


# test that bus factor calculation returns a correct score
def test_bus_factor():
    stats_contributors = GithubHelper.get_stats_contributors('cloudinary/cloudinary_npm')
    commits = GithubHelper.get_commits('cloudinary/cloudinary_npm')
    bus_factor = BusFactor(5, 'cloudinary/cloudinary_npm', stats_contributors, commits)

    bus_factor.calculate_score()

    if bus_factor.score > 0.5: return 1
    else: return 0


# test that bus factor calculation returns a correct score
def test_bus_factor_none():
    stats_contributors = None
    commits = None
    bus_factor = BusFactor(5, 'cloudinary/cloudinary_npm', stats_contributors, commits)

    bus_factor.calculate_score()

    if bus_factor.score == 0: return 1
    else: return 0


# test that bus factor calculation returns a correct score
def test_bus_factor_empty():
    stats_contributors = []
    commits = []
    bus_factor = BusFactor(5, 'cloudinary/cloudinary_npm', stats_contributors, commits)

    bus_factor.calculate_score()

    if bus_factor.score == 0: return 1
    else: return 0


# test that npm urls convert to github urls correctly
def test_npm_to_github():
    npm_urls = ['cloudinary', 'even', 'express', 'browserify']
    github_urls = ['https://github.com/cloudinary/cloudinary_npm',
                   'https://github.com/jonschlinkert/even',
                   'https://github.com/expressjs/express',
                   'https://github.com/browserify/browserify']

    correct = 0
    for i in range(len(npm_urls)):
        val = GithubHelper.get_path(GithubHelper.url_from_npm(npm_urls[i]))
        val = 'https://github.com/' + str(val)
        if val == github_urls[i]:
            correct += 1

    if correct == len(npm_urls): return 1
    else: return 0


def test_responsiveness():
    open_issues, closed_issues = GithubHelper.get_issues('expressjs/express')
    resp = Responsiveness('expressjs/express', 'https://github.com/expressjs/express', open_issues, closed_issues, 0)

    resp.calculate_responsiveness()

    if resp.score > 0.5: return 1
    else: return 0


def test_responsiveness_no_issues():
    open_issues, closed_issues = GithubHelper.get_issues('jonschlinkert/even')
    resp = Responsiveness('jonschlinkert/even', 'https://github.com/jonschlinkert/even', open_issues, closed_issues, 0)

    resp.calculate_responsiveness()

    if resp.score == 0.5: return 1
    else: return 0


def test_ramp_up():
    # Get popularity
    name = 'expressjs/express'
    url = 'https://github.com/expressjs/express'
    popularity = Popularity(name, url)
    popularity_score = popularity.calculate_popularity()

    # Get responsiveness
    open_issues, closed_issues = GithubHelper.get_issues('expressjs/express')
    resp = Responsiveness(name, url, open_issues, closed_issues, 0)
    resp.calculate_responsiveness()

    # Get correctness
    correctness = Correctness(name, open_issues, closed_issues, [], popularity_score)
    correctness.calculate_score()

    # Calculate RampUp
    ugh = Module(name, url, url)
    ugh.clone_repo()
    ramp_up = RampUp(name, url, popularity_score, 0)
    ramp_up.calculate_ramp_up(resp.score, correctness.score)
    ugh.remove_repo()

    if ramp_up.score > 0.5: return 1
    else: return 0


def test_ramp_up_low():
    # Get popularity
    name = 'jonschlinkert/even'
    url = 'https://github.com/jonschlinkert/even'
    popularity = Popularity(name, url)
    popularity_score = popularity.calculate_popularity()

    # Get responsiveness
    open_issues, closed_issues = GithubHelper.get_issues('jonschlinkert/even')
    resp = Responsiveness(name, url, open_issues, closed_issues, 0)
    resp.calculate_responsiveness()

    # Get correctness
    correctness = Correctness(name, open_issues, closed_issues, [], popularity_score)
    correctness.calculate_score()

    # Calculate RampUp
    ugh = Module(name, url, url)
    ugh.clone_repo()
    ramp_up = RampUp(name, url, popularity_score, 0)
    ramp_up.calculate_ramp_up(resp.score, correctness.score)
    ugh.remove_repo()

    if ramp_up.score < 0.6: return 1
    else: return 0


def test_get_users():
    num_users = get_number_users('https://github.com/expressjs/express')
    if num_users > 1000000: return 1
    else: return 0


def test_get_users_low():
    num_users = get_number_users('https://github.com/jonschlinkert/even')
    if num_users is None: return 1
    else: return 0


def test_get_users_zero():
    num_users = get_number_users('https://github.com/sguadav/Predicting_soccer_results')
    if num_users is None: return 1
    else: return 0


def test_popularity():
    popularity = Popularity('expressjs/express', 'https://github.com/expressjs/express')
    popularity_score = popularity.calculate_popularity()
    if popularity_score > 0.5: return 1
    else: return 0


def test_popularity_low():
    popularity = Popularity('jonschlinkert/even', 'https://github.com/jonschlinkert/even')
    popularity_score = popularity.calculate_popularity()
    if popularity_score < 0.5: return 1
    else: return 0


def test_correctness_low():
    path = 'nullivex/nodist'
    open_issues, closed_issues = GithubHelper.get_issues(path)
    priority = 5
    popularity = Popularity(path, 'https://github.com/nullivex/nodist')
    popularity_score = popularity.calculate_popularity()
    correctness = Correctness(path, open_issues, closed_issues, priority, popularity_score)
    if correctness.score < 0.5: return 1
    else: return 0


def test_correctness_high():
    path = 'cloudinary/cloudinary_npm'
    open_issues, closed_issues = GithubHelper.get_issues(path)
    priority = 5
    popularity = Popularity(path, 'https://github.com/cloudinary/cloudinary_npm')
    popularity_score = popularity.calculate_popularity()
    correctness = Correctness(path, open_issues, closed_issues, priority, popularity_score)
    correctness.calculate_score()
    if correctness.score > 0.5: return 1
    else: return 0


def test_license_low():
    path = 'dbatides/3issues_2commits'
    priority = 5
    readMe = GithubHelper.get_readme(path)
    license = License(path, priority, readMe)
    license.calculate_score()
    if license.score == 0: return 1
    else: return 0


def test_license_high():
    path = 'cloudinary/cloudinary_npm'
    priority = 5
    readMe = GithubHelper.get_readme(path)
    license = License(path, priority, readMe)
    license.calculate_score()
    if license.score == 1: return 1
    else: return 0


def test_weights_general():
    path = 'johnthebrit/RandomStuff'
    url = 'https://github.com/johnthebrit/RandomStuff'
    module = Module(path, url, url)
    open_issues, closed_issues = GithubHelper.get_issues(path)
    readMe = GithubHelper.get_readme(path)
    stats_contributors = GithubHelper.get_stats_contributors(path)
    commits = GithubHelper.get_commits(path)

    module.correct_class = Correctness(path, open_issues, closed_issues, 5, 0)
    module.license_class = License(path, 5, readMe)
    module.bus_factor_class = BusFactor(5, path, stats_contributors, commits)
    module. responsiveness_class = Responsiveness(path, url, open_issues, closed_issues, 5)
    module.ramp_up_class = RampUp(path, url, 0, 5)
    module.dependency_class = Dependency(path, url, 5)

    module.get_weights()
    if module.weights == [0.17, 0.17, 0.17, 0.17, 0.17, 0.17]: return 1
    else: return 0


def test_weights_specific():
    path = 'SadProcessor/SomeStuff'
    url = 'https://github.com/SadProcessor/SomeStuff'
    module = Module(path, url, url)
    open_issues, closed_issues = GithubHelper.get_issues(path)
    readMe = GithubHelper.get_readme(path)
    stats_contributors = GithubHelper.get_stats_contributors(path)
    commits = GithubHelper.get_commits(path)

    module.correct_class = Correctness(path, open_issues, closed_issues, 2, 0)
    module.license_class = License(path, 5, readMe)
    module.bus_factor_class = BusFactor(4, path, stats_contributors, commits)
    module. responsiveness_class = Responsiveness(path, url, open_issues, closed_issues, 7)
    module.ramp_up_class = RampUp(path, url, 0, 2)
    module.dependency_class = Dependency(path, url, 4)

    module.get_weights()
    if module.weights == [0.29, 0.21, 0.17, 0.08, 0.08, 0.17]: return 1
    else: return 0

def test_dependency_low():
    dep = Dependency('TrustworthyModules/test_dep/dep_low', '', 4)
    dep.calculate_score()
    if dep.score < 0.2: return 1
    else: return 0

def test_dependency_high():
    dep = Dependency('TrustworthyModules/test_dep/dep_high', '', 4)
    dep.calculate_score()
    if dep.score > 0.8: return 1
    else: return 0

def test_dependency_zero():
    dep = Dependency('TrustworthyModules/test_dep/dep_zero', '', 4)
    dep.calculate_score()
    if dep.score == 0.0: return 1
    else: return 0


def call_tests():
    num_passed = 0
    total = 29

    num_passed += test_end_to_end_even()
    num_passed += test_end_to_end_jquery()
    num_passed += test_verify_path()
    #num_passed += test_read_input()
    num_passed += test_calculate_std()
    num_passed += test_total_contributors()
    num_passed += test_get_commits()
    num_passed += test_get_year_commit_ratio()
    num_passed += test_bus_factor()
    num_passed += test_bus_factor_none()
    num_passed += test_bus_factor_empty()
    num_passed += test_npm_to_github()
    num_passed += test_responsiveness()
    num_passed += test_responsiveness_no_issues()
    num_passed += test_ramp_up()
    num_passed += test_ramp_up_low()
    num_passed += test_get_users()
    num_passed += test_get_users_low()
    num_passed += test_get_users_zero()
    num_passed += test_popularity()
    num_passed += test_popularity_low()
    num_passed += test_correctness_low()
    num_passed += test_correctness_high()
    num_passed += test_license_low()
    num_passed += test_license_high()
    num_passed += test_weights_general()
    num_passed += test_weights_specific()
    num_passed += test_dependency_high()
    num_passed += test_dependency_low()
    num_passed += test_dependency_zero()

    return (num_passed, total)