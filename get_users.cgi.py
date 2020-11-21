#!/usr/bin/env python3
import sys
import os
import json
from urllib.parse import parse_qs
import configparser
import random
import redis

#### \\\\ #### //// ####

def printCGI(text):
	print("Content-type: application/json\n")
	print(text)
	sys.exit(0)

#### //// #### \\\\ ####

args = parse_qs(os.environ['QUERY_STRING'])
result = {'result': [], 'success': True}

limit = int(args['limit'][0])
if limit > 50 or limit < 1:
	result['success'] = False
	printCGI(json.dumps(result))

config = configparser.ConfigParser() # Настройки
config.read("settings.ini")

r = redis.Redis(host=config['Redis']['host'],
	port=int(config['Redis']['port']),
	db=int(config['Redis']['db']))

pu_range = max(1, int(limit / 100 * 20)) # Просто на всякий случай :^)
pu = r.srandmember('priority_users_shuffled', pu_range)
u = r.srandmember('users_shuffled', limit - pu_range)

if len(pu) == 0 or len(u) == 0:
	result['success'] = False
	printCGI(json.dumps(result))

for x in pu:
	result['result'].append(int(x))
for x in u:
	result['result'].append(int(x))
random.shuffle(result['result'])

printCGI(json.dumps(result))
