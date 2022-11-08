from bs4 import BeautifulSoup
import requests
import json


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    result = requests.get(url, headers=headers)
    return BeautifulSoup(result.content.decode(), features='lxml')

def lst2txt(file, lst):
    assert type(file) == str
    assert type(lst) == list
    with open(file, 'w') as f:
        for item in lst:
            f.write(f"{item}\n")

def txt2lst(file):
    assert type(file) == str
    with open(file, 'r') as f:
        return f.read().splitlines()

def load_data():
    with open('data/matchups.json', 'r') as f:
        return json.load(f)
