import json
import pandas as pd

with open('data/protests.json', 'r') as f:
    protests = json.load(f)

protests_list = []

for state in protests:
    state_name = list(state.keys())[0]
    for protest in state[state_name]:
        protests_list.append({'state': state_name,
                              'loc': protest['loc'],
                              'description': protest['description']})

pd.DataFrame(protests_list).to_csv('data/protests.csv', index=False)
