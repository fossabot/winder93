#!/usr/bin/env python3
import os
from urllib.parse import parse_qs

print("Content-type: application/json\n")

print(parse_qs(os.environ['QUERY_STRING']))
