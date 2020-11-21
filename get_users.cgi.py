#!/usr/bin/env python3
import os

print("Content-type: application/json\n")
print(os.environ['QUERY_STRING'])
