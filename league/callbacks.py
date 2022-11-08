import dearpygui.dearpygui as dpg
from util import load_data

roles = ['top', 'jungle', 'mid', 'adc', 'support']
matchup = [['', ''],
           ['', ''],
           ['', ''],
           ['', ''],
           ['', '']]
data = load_data()

def update_winrate(sender, app_data, user_data):
    START_ID = 30
    champion = app_data if '(' not in app_data else app_data[:app_data.index('(') - 1]

    row, col = (sender - START_ID) // 5, (sender - START_ID) % 5
    role = roles[row]
    matchup[row][col] = champion
    ally, enemy = matchup[row]

    if ally != '' and enemy != '' and enemy in data[role][ally]:
        winrate = data[role][ally][enemy]['winrate']
        games = data[role][ally][enemy]['games']
        dpg.set_value(f"{role}_winrate", f'{winrate}% ({games})')
    else:
        dpg.set_value(f"{role}_winrate", '')

    team = 'ally' if col == 0 else 'enemy'
    if team == 'enemy':
        if champion == '':
            new_combo = [''] + list(data[role].keys())
        else:
            new_combo = [''] + [f'{c} ({round(100 - s["winrate"], 2)}%)' for c, s in sorted(data[role][champion].items(), key=lambda x: x[1]['winrate'])]
        dpg.configure_item(sender - 1, items=new_combo)

    winrates = []
    games = []
    for role, (ally, enemy) in zip(roles, matchup):
        if ally != '' and enemy != '':
            winrates.append(data[role][ally][enemy]['winrate'])
            games.append(data[role][ally][enemy]['games'])
    if len(winrates) > 0:
        average_winrate = round(sum(winrates) / len(winrates), 2)
        weighted_winrate = round(sum([w * g / sum(games) for w, g in zip(winrates, games)]), 2)
        dpg.set_value("average_winrate", average_winrate)
        dpg.set_value("weighted_winrate", weighted_winrate)
    else:
        dpg.set_value("average_winrate", '')
        dpg.set_value("weighted_winrate", '')



