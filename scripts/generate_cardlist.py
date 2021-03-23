import glob
import tarfile
import os
from pyquery import PyQuery
import json

def parse_supply(supply_string):
    pq = PyQuery(supply_string)
    cardnames = [item.text() for item in pq('span').items()]
    cardtypes = [item.attr("class") for item in pq('span').items()]
    return(cardnames, cardtypes)

def get_cards(filename):
    input_file = open(filename, 'r')
    supply_line = input_file.readlines()[3]
    # parse initial supply
    cardnames, cardtypes = parse_supply(supply_line)
    return cardnames, cardtypes

# Unpack each tar file individually and process gamelogs to save space

tarfiles = glob.glob('../data/*.tar.bz2')[:1]
# Temporary directory to hold unpacked files
try:
    os.mkdir('../data/tmp')
except:
    pass

data = {}
data['kingdom_cards'] = []
existing_cardnames = []
for filename in tarfiles:
        tar = tarfile.open(filename, "r:bz2")
        tar.extractall('../data/tmp')
        tar.close()
        gamelogs = glob.glob('../data/tmp/*')
        for gamelog in gamelogs:
            cardnames, cardtypes = get_cards(gamelog)
            for i in range(len(cardnames)):
                name = cardnames[i]
                type = cardtypes[i]
                starting_number = 10
                if 'victory' in type:
                    starting_number = 8
                if not name in existing_cardnames:
                    data['kingdom_cards'].append({
                        'name': name,
                        'type': type,
                        'starting_number': starting_number
                    })
                    existing_cardnames.append(name)
            os.remove(gamelog)

with open('../data/kingdom_cards.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)

os.rmdir('../data/tmp')


