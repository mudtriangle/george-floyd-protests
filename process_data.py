import json
import pandas as pd
import urllib.parse

with open('data/protests.json', 'r') as f:
    protests = json.load(f)

protests_list = []

for state in protests:
    state_name = list(state.keys())[0]
    for protest in state[state_name]:
        refs = []
        for ref in protest['refs']:
            els = ref.split('&')
            link = urllib.parse.unquote(els[-2][len('rft_id='):])
            refs.append(link)

        protests_list.append({'state': state_name,
                              'loc': protest['loc'],
                              'description': protest['description'],
                              'url': protest['url'],
                              'refs': '\t'.join(refs)})

pd.DataFrame(protests_list).to_csv('data/protests.csv', index=False)
