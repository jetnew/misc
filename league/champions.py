from util import get_soup, lst2txt

soup = get_soup('https://www.op.gg/champions')
all_champions = [n.text for n in soup.find_all('a', {'class': 'css-mtyeel'})]
lst2txt('data/all.txt', all_champions)

roles = ['top', 'jungle', 'mid', 'adc', 'support']
for role in roles:
    soup = get_soup(f'https://www.op.gg/champions?position={role}')

    champions = [n.text for n in soup.find_all('td', {'class': 'css-cym2o0'})]
    lst2txt(f'data/{role}_name.txt', champions)

    champions = [n.find('a').get('href').split('/')[2] for n in soup.find_all('td', {'class': 'css-cym2o0'})]
    lst2txt(f'data/{role}_url.txt', champions)