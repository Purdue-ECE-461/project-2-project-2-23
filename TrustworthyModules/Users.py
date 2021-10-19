import requests
from bs4 import BeautifulSoup as bs


def get_number_users(url):
    # Use Web Scraping to get the number of users in a repository using Beautiful Soup
    response = requests.get(url, headers={"User-Agent": "Chrome"})
    response_code = response.status_code
    if response_code != 200:
        return None
    html_content = response.content
    dom = bs(html_content, 'html.parser')
    users_find = dom.find_all("span", class_="px-2 text-bold text-small no-wrap")

    if len(users_find) == 0:
        return None

    num_user = int(users_find[0].text.replace(" ", "").replace("+", "").replace("\n", "").replace(",", ""))
    return num_user
