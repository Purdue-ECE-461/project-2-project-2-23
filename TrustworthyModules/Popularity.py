from TrustworthyModules.Util import get_logger
import TrustworthyModules.GithubHelper as GithubHelper
import TrustworthyModules.Users as Users

logger = get_logger('Popularity')
logger.info("Logger init in Popularity.py")

SUBSCRIBERS_MAX = 1000
WATCHERS_MAX = 40000
FORKS_MAX = 5000
STARGAZERS_MAX = 40000
USERS_MAX = 3000000  # 3,000,000


class Popularity:
    def __init__(self, module_path, url):
        self.module_path = module_path
        self.url = url
        self.subscribers = 0
        self.watchers = 0
        self.forks = 0
        self.stargazers = 0
        self.users = 0
        self.contributors = 0

    def get_attributes(self):
        self.subscribers = GithubHelper.get_subscribers(self.module_path).totalCount
        self.watchers = GithubHelper.get_watchers(self.module_path).totalCount
        self.forks = GithubHelper.get_forks(self.module_path).totalCount
        self.stargazers = GithubHelper.get_stargazers(self.module_path).totalCount
        self.users = Users.get_number_users(self.url)
        self.contributors = GithubHelper.get_contributors(self.module_path).totalCount

    def calculate_popularity(self):
        logger.debug(f"Calculating Popularity for {self.module_path}")

        self.get_attributes()

        temp = self.calculate_subscriber_pop()
        sub = temp if temp <= 1 else 1

        temp = self.calculate_watcher_pop()
        watch = temp if temp <= 1 else 1

        temp = self.calculate_forks_pop()
        fork = temp if temp <= 1 else 1

        temp = self.calculate_stargazers_pop()
        star = temp if temp <= 1 else 1

        if self.users is not None:
            temp = self.calculate_contributors_influence()
            contribute = temp if temp <= 1 else 1

            temp = self.calculate_users_pop()
            users = temp if temp <= 1 else 1

            # Total calculation if module users found
            popularity = round((sub + watch + fork + star + (0.25 + (0.75 * users)) + contribute) / 6, 4)
        else:
            # Total calculation if not module users found
            popularity = round((sub + watch + fork + star) / 4, 4)

        logger.debug(f"Popularity: final score calculated {popularity}")

        return popularity  # 1 = max popularity, 0 = min

    def calculate_subscriber_pop(self):
        return self.subscribers / SUBSCRIBERS_MAX

    def calculate_watcher_pop(self):
        return self.watchers / WATCHERS_MAX

    def calculate_forks_pop(self):
        return self.forks / FORKS_MAX

    def calculate_stargazers_pop(self):
        return self.watchers / STARGAZERS_MAX

    def calculate_users_pop(self):
        return self.users / USERS_MAX

    def calculate_contributors_influence(self):
        ratio = self.contributors / self.users

        output = 1
        users = 1000  # number could be tweaked
        count = 0

        while output > ratio:
            output = 1 / users
            users += 1000  # number could be tweaked
            count += 1

        # print("!!!! count !!!!")
        score = 1 - (count * .025)  # number could be tweaked
        if score < 0:
            score = 0
        elif score > 1:
            score = 1
        # essentially worth 2.5% for every 1 collaborator : 1000 users
        # negatively effects largely used modules but other variables above should increase overall popularity score

        # print(count, module.contributors.totalCount, module.users, score)

        return score

