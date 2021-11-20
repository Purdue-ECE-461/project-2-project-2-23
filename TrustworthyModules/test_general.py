import datetime
import pytest
import sys

from Module import Module
import Main
import IOUtil
import GithubHelper
from Users import get_number_users
from Contributor import Contributor
from Correctness import Correctness
from License import License
from BusFactor import BusFactor, calculate_std
from Popularity import Popularity
from Responsiveness import Responsiveness
from RampUp import RampUp
from Dependency import Dependency


# end to end test of low performing repo
def test_end_to_end_even():
    module_list = Main.run_rank_mode('test_files/even.txt')
    assert module_list[0] < 0.8


# end to end test of high performing repo
def test_end_to_end_jquery():
    module_list = Main.run_rank_mode('test_files/single_test_file.txt')
    assert module_list[0] > 0.5


# check that an invalid path is caught
def test_verify_path():
    assert IOUtil.verify_path("xxd") == -1


# check that input files are read properly
def test_read_input():
    assert IOUtil.read_input_file('test_files/test_file') == ["https://github.com/jquery/jquery"]


# validate standard deviation calculation in BusFactor
def test_calculate_std():
    assert calculate_std([1, 1, 1, 1]) - 0.195959 < 0.001


# test that correct number of total contributors is obtained in BusFactor creation
def test_total_contributors():
    sample_mod = Module('jonschlinkert/even', 'https://github.com/jonschlinkert/even', 'https://github.com/jonschlinkert/even')
    sample_mod.stats_contributors = GithubHelper.get_stats_contributors('jonschlinkert/even')
    wks = sample_mod.stats_contributors[0].weeks

    c1 = Contributor.Contributor('me', 90, wks, '1')
    c2 = Contributor.Contributor('me', 90, wks, '1')
    c3 = Contributor.Contributor('me', 89, wks, '1')

    busObj = BusFactor(7, 'test', [c1, c2, c3], None)

    total_cont = busObj.total_contributors

    assert total_cont == 3


# test that the correct number of commits is fetched
def test_get_commits():
    commits = GithubHelper.get_commits('jonschlinkert/eval-estree-expression')
    count = commits.totalCount
    assert count >= 32


# test that the correct commit ratio for the past year is calculated
def test_get_year_commit_ratio():
    if datetime.date.today() > datetime.date(2022, 7, 18):
        pytest.skip("Past a year from initial commit; cannot ensure test validity")

    commits = GithubHelper.get_commits('jonschlinkert/eval-estree-expression')
    ratio = GithubHelper.last_year_commit_ratio('jonschlinkert/eval-estree-expression', commits)
    assert ratio == 1.0


# test that bus factor calculation returns a correct score
def test_bus_factor():
    stats_contributors = GithubHelper.get_stats_contributors('cloudinary/cloudinary_npm')
    commits = GithubHelper.get_commits('cloudinary/cloudinary_npm')
    bus_factor = BusFactor(5, 'cloudinary/cloudinary_npm', stats_contributors, commits)

    bus_factor.calculate_score()

    assert bus_factor.score > 0.5


# test that bus factor calculation returns a correct score
def test_bus_factor_none():
    stats_contributors = None
    commits = None
    bus_factor = BusFactor(5, 'cloudinary/cloudinary_npm', stats_contributors, commits)

    bus_factor.calculate_score()

    assert bus_factor.score == 0

# test that bus factor calculation returns a correct score
def test_bus_factor_empty():
    stats_contributors = []
    commits = []
    bus_factor = BusFactor(5, 'cloudinary/cloudinary_npm', stats_contributors, commits)

    bus_factor.calculate_score()

    assert bus_factor.score == 0


# test that npm urls convert to github urls correctly
def test_npm_to_github():
    npm_urls = ['cloudinary', 'even', 'express', 'browserify']
    github_urls = ['https://github.com/cloudinary/cloudinary_npm',
                   'https://github.com/jonschlinkert/even',
                   'https://github.com/expressjs/express',
                   'https://github.com/browserify/browserify']

    correct = 0
    for i in range(len(npm_urls)):
        val = GithubHelper.get_repo_path(GithubHelper.url_from_npm(npm_urls[i]))
        val = 'https://github.com/' + str(val)
        if val == github_urls[i]:
            correct += 1

    assert correct == len(npm_urls)


def test_responsiveness():
    open_issues, closed_issues = GithubHelper.get_issues('expressjs/express')
    resp = Responsiveness('expressjs/express', 'https://github.com/expressjs/express', open_issues, closed_issues, 0)

    resp.calculate_responsiveness()

    assert resp.score > 0.5


def test_responsiveness_no_issues():
    open_issues, closed_issues = GithubHelper.get_issues('jonschlinkert/even')
    resp = Responsiveness('jonschlinkert/even', 'https://github.com/jonschlinkert/even', open_issues, closed_issues, 0)

    resp.calculate_responsiveness()

    assert resp.score == 0.5


def test_ramp_up():
    # Get popularity
    popularity = Popularity('expressjs/express', 'https://github.com/expressjs/express')
    popularity_score = popularity.calculate_popularity()

    # Get responsiveness
    open_issues, closed_issues = GithubHelper.get_issues('expressjs/express')
    resp = Responsiveness('expressjs/express', 'https://github.com/expressjs/express', open_issues, closed_issues, 0)
    resp.calculate_responsiveness()

    # Get correctness
    correctness = Correctness('expressjs/express', open_issues, closed_issues, [], popularity_score)
    correctness.calculate_score()

    # Calculate RampUp
    ramp_up = RampUp('expressjs/express', 'https://github.com/expressjs/express', popularity_score, 0)
    ramp_up.calculate_ramp_up(resp.score, correctness.score)

    assert ramp_up.score > 0.5


def test_ramp_up_low():
    # Get popularity
    popularity = Popularity('jonschlinkert/even', 'https://github.com/jonschlinkert/even')
    popularity_score = popularity.calculate_popularity()

    # Get responsiveness
    open_issues, closed_issues = GithubHelper.get_issues('expressjs/express')
    resp = Responsiveness('jonschlinkert/even', 'https://github.com/jonschlinkert/even', open_issues, closed_issues, 0)
    resp.calculate_responsiveness()

    # Get correctness
    correctness = Correctness('jonschlinkert/even', open_issues, closed_issues, [], popularity_score)
    correctness.calculate_score()

    # Calculate RampUp
    ramp_up = RampUp('jonschlinkert/even', 'https://github.com/jonschlinkert/even', popularity_score, 0)
    ramp_up.calculate_ramp_up(resp.score, correctness.score)

    assert ramp_up.score < 0.6


def test_get_users():
    num_users = get_number_users('https://github.com/expressjs/express')
    assert num_users > 1000000


def test_get_users_low():
    num_users = get_number_users('https://github.com/jonschlinkert/even')
    assert num_users is None


def test_get_users_zero():
    num_users = get_number_users('https://github.com/sguadav/Predicting_soccer_results')
    assert num_users is None


def test_popularity():
    popularity = Popularity('expressjs/express', 'https://github.com/expressjs/express')
    popularity_score = popularity.calculate_popularity()
    assert popularity_score > 0.5


def test_popularity_low():
    popularity = Popularity('jonschlinkert/even', 'https://github.com/jonschlinkert/even')
    popularity_score = popularity.calculate_popularity()
    assert popularity_score < 0.5


def test_correctness_low():
    path = 'nullivex/nodist'
    open_issues, closed_issues = GithubHelper.get_issues(path)
    priority = 5
    popularity = Popularity(path, 'https://github.com/nullivex/nodist')
    popularity_score = popularity.calculate_popularity()
    correctness = Correctness(path, open_issues, closed_issues, priority, popularity_score)
    assert correctness.score < 0.5


def test_correctness_high():
    path = 'cloudinary/cloudinary_npm'
    open_issues, closed_issues = GithubHelper.get_issues(path)
    priority = 5
    popularity = Popularity(path, 'https://github.com/cloudinary/cloudinary_npm')
    popularity_score = popularity.calculate_popularity()
    correctness = Correctness(path, open_issues, closed_issues, priority, popularity_score)
    correctness.calculate_score()
    assert correctness.score > 0.5


def test_license_low():
    path = 'Purdue-ECE-461/project-1-team-22'
    priority = 5
    readMe = GithubHelper.get_readme(path)
    license = License(path, priority, readMe)
    license.calculate_score()
    assert license.score == 0


def test_license_high():
    path = 'cloudinary/cloudinary_npm'
    priority = 5
    readMe = GithubHelper.get_readme(path)
    license = License(path, priority, readMe)
    license.calculate_score()
    assert license.score == 1


def test_weights_general():
    path = 'Purdue-ECE-461/project-1-team-22'
    url = 'https://github.com/Purdue-ECE-461/project-1-team-22'
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

    module.get_weights()
    assert module.weights == [.2, .2, .2, .2, .2]


def test_weights_specific():
    path = 'Purdue-ECE-461/project-1-team-22'
    url = 'https://github.com/Purdue-ECE-461/project-1-team-22'
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

    module.get_weights()
    assert module.weights == [.35, .25, .2, .1, .1]


if __name__ == "__main__":
    test_npm_to_github()
    test_read_input()
    test_verify_path()
    test_end_to_end_jquery()
    test_end_to_end_even()
    test_calculate_std()
    test_responsiveness()
    test_responsiveness_no_issues()
    test_ramp_up()
    test_ramp_up_low()
    test_get_users()
    test_get_users_low()
    test_get_users_zero()
    test_popularity()
    test_popularity_low()
    test_correctness_low()
    test_correctness_high()
    test_license_low()
    test_license_high()
    test_weights_general()
    test_weights_specific()

