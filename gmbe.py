import requests
from bs4 import BeautifulSoup as bs
import os
import codecs
import argparse
from markdownify import markdownify as md

URL = 'https://codechalleng.es/bites/'
GIT_LOGIN = 'https://github.com/session'
URL_LOGIN = 'https://codechalleng.es/oauth/login/github/?next='

if not os.path.exists('.password_git'):
    print("You need to have .password_git file with git login password separated by space")
    raise FileExistsError

USER, PASSWORD = open('.password_git', mode='r').read().split()

def _get_response(login=USER, password=PASSWORD, bite=82):
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    login_data = {
        'commit': 'Sign in',
        'utf8': '%E2%9C%93',
        'login': login,
        'password': password
    }

    with requests.Session() as s:
        soup = bs(s.get(GIT_LOGIN, headers=headers).content, 'html.parser')
        login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
        s.post(GIT_LOGIN, data=login_data, headers=headers)
        s.get(URL_LOGIN)
        response = s.get(URL+str(bite))

    return response


def _save_file(path, name, content):
    full_path = os.path.join(path, name)
    if not os.path.exists(path):
        os.makedirs(path)

    if os.path.exists(full_path):
        raise FileExistsError

    with codecs.open(full_path, 'w', 'utf-8') as fl:
        fl.write(content)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bite', dest='bite', required=True, metavar='BITE', help='Bite to download')
    return parser


if __name__ == "__main__":
    args = create_parser().parse_args()
    bite = int(args.bite)
    response = _get_response(bite=bite)
    soup = bs(response.content, 'html.parser')
    code_name, test_name = [a.text[1:-1] for a in soup.find_all("span", {"class": "smallerFont"})]
    code_text = soup.find(id="editor").text
    test_text = soup.find(id="secondEditor").text
    task_text = md(' '.join(map(str, soup.find("blockquote", {"class": "biteDescription"}).contents)))
    _save_file(str(bite), code_name, code_text)
    _save_file(str(bite), test_name, test_text)
    _save_file(str(bite), f'bite_{bite}.md', task_text)



