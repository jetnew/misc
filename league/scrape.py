from util import get_soup, txt2lst
import json

# all_champions = txt2lst('data/all.txt')
roles = ['top', 'jungle', 'mid', 'adc', 'support']

dataset = {}
for role in roles:
    dataset[role] = {}
    urls = txt2lst(f'data/{role}_url.txt')
    names = txt2lst(f'data/{role}_name.txt')

    for i, (name, url) in enumerate(zip(names, urls)):
        print(f'Role={role}, Champion={name} {i+1}/{len(names)} champions')
        dataset[role][name] = {}
        soup = get_soup(f'https://www.op.gg/champions/{url}/{role}/counters')

        table = soup.find('table', {'class': 'css-4hiot4'})
        matchups = [m.text for m in table.find_all('div', {'class': 'css-aj4kza'})]
        winrates = [float(w.text[:-1]) for w in table.find_all('span', {'class': 'css-ekbdas'})]
        games = [int(g.text.replace(',', '')) for g in table.find_all('span', {'class': 'css-1nfew2i'})]

        assert len(matchups) == len(winrates) == len(games)
        for matchup, winrate, game in zip(matchups, winrates, games):
            dataset[role][name][matchup] = dict(winrate=winrate, games=game)


with open('data/matchups.json', 'w') as f:
    json.dump(dataset, f)
