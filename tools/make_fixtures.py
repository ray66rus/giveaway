import random
import time
import json 

def create_clients():
	data = list()
	for i, l in enumerate(open('names.txt', encoding='utf-8')):
		name, fname, patr = l.split();
		data.append({
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
	    json.dump(data, outfile, indent=4)


def create_giveaways():
	data = list()
	counter = 0
	for i in range(100):
		for j in range(random.randint(0, 3)):
			date = list(time.localtime(time.time()))
			date[2] = random.randint(1, date[2])
			goods = random.randint(1, 6)
			data.append({
				'model': 'giveaway.giveaway',
				'pk': counter,
				'fields': {
					'date': time.strftime('%Y-%m-%d', tuple(date)),
					'goods_number' : goods,
					'client_id': i
				}
			})
			counter += 1
	
	with open('giveaways.json', 'w') as outfile:
	    json.dump(data, outfile, indent=4)


create_clients()
create_giveaways()
