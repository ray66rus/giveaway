import random
import time
import json
from functools import reduce

def create_clients():
	clients = list()
	for i, l in enumerate(open('names.txt', encoding='utf-8')):
		fname, name, patr = l.split();
		clients.append({
			'model': 'giveaway.client',
			'pk': i,
			'fields': {
				'first_name': name,
				'last_name': fname,
				'patronymic': patr,
				'year_of_birth': random.randint(1950, 2000)
			}
		})

	with open('clients.json', 'w') as outfile:
	    json.dump(clients, outfile, indent=4)

	return clients


def create_giveaways(clients):
    giveaways = list()
    for i, client in enumerate(clients):
        random.seed(_calculate_client_number(client))
        for j in range(12):
            giveaways += _add_giveaways_for_month(j, client_id=i)

    with open('giveaways.json', 'w') as outfile:
        json.dump(giveaways, outfile, indent=4)

    return giveaways


def _calculate_client_number(client):
	return reduce(lambda a, f: a + len(str(f)), client['fields'].values(), 0)

def _add_giveaways_for_month(m, client_id):
    giveaways = list()
    date = list(time.localtime(time.time()))
    date[1] = m
    for i in range(random.randint(0, 3)):
        date[2] = random.randint(1, 28)
        goods = random.randint(1, 6)
        giveaways.append({
            'model': 'giveaway.giveaway',
            'pk': client_id*1000 + m * 10 + i,
            'fields': {
                'date': time.strftime('%Y-%m-%d', tuple(date)),
                'goods_number' : goods,
                'client': client_id
            }
        })

    return giveaways


clients = create_clients()
create_giveaways(clients)
