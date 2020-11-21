#!/usr/bin/env python3
import os
import json
from urllib.parse import parse_qs
import configparser
import random
import redis

args = parse_qs(os.environ['QUERY_STRING'])
result = {'result': [], 'success': True}

if 'limit' not in args:
	args['limit'] = '50'
elif int(args['limit']) > 50 or int(args['limit']) < 1:
	args['limit'] = '1'
limit = int(args['limit']) - 1

config = configparser.ConfigParser() # Настройки
config.read("settings.ini")

r = redis.Redis(host=config['Redis']['host'],
	port=int(config['Redis']['port']),
	db=int(config['Redis']['db']))

pu_range = min(0, int(limit / 100 * 20)) # Просто на всякий случай :^)
pu = r.srandmember('priority_users_shuffled', pu_range)
u = r.srandmember('users_shuffled', limit - pu_range)

if len(pu) == 0 or len(u) == 0:
	result['success'] = False
else:
	for x in pu:
		result['result'].append(int(x))
	for x in u:
		result['result'].append(int(x))

#### //// #### \\\\ ####

print("Content-type: application/json\n")
print(json.dumps(result))
