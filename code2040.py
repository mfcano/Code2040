import requests, json, re
import datetime  
from datetime import timedelta  
import time
""" Hello! My name is Mauricio Cano. I'm a student at Carnegie Mellon University. I wanted to take this opportunity
to thank you (whoever is looking over this stuff) for taking the time to look at my work and the essays I've 
written! I look forward to hearing from you :)
"""

payload = {'email': 'msephr@gmail.com', 'github': 'https://github.com/mfcano/Code2040'}
r = requests.post("http://challenge.code2040.org/api/register", data=json.dumps(payload))

def eval_r(dictionary):
	return eval(dictionary)["result"]

token = eval_r(r.content)
request_payload = {'token': token}


# Stage 1
raw_out = requests.post("http://challenge.code2040.org/api/getstring", data=json.dumps(request_payload))

string = eval_r(raw_out.content)
string = string[::-1]

payload = {'token': token, 'string': string}
result = requests.post("http://challenge.code2040.org/api/validatestring", data=json.dumps(payload))


# Stage 2
raw_out = requests.post("http://challenge.code2040.org/api/haystack", data=json.dumps(request_payload))
#print eval_r(raw_out.content)
needle = eval_r(raw_out.content)["needle"]
haystack = eval_r(raw_out.content)["haystack"]

#Easy way ->
index = haystack.index(needle)

#In languages without such nice functions:
for i in xrange(len(haystack) - 1):
	if haystack[i] == needle:
		index = i
		break

payload = {'token': token, 'needle': index}

result = requests.post("http://challenge.code2040.org/api/validateneedle", data=json.dumps(payload))



#Stage 3:

raw_out = requests.post("http://challenge.code2040.org/api/prefix", data=json.dumps(request_payload))

array = eval_r(raw_out.content)["array"]
prefix = eval_r(raw_out.content)["prefix"]

final_list = [i for i in array if (prefix not in i)]
	
payload = {'token': token, 'array': final_list}
result = requests.post("http://challenge.code2040.org/api/validateprefix", data=json.dumps(payload))


#Stage 4:

def parse_datestamp(datestamp):
	datestamp = datestamp.replace("T", "-")
	datestamp = datestamp.replace(":", "-")
	datestamp = datestamp.replace(".", "-")
	datestamp = datestamp.replace("Z", "")
	data = datestamp.split("-")
	intdata = []
	for x in data:
		intdata += [int(x)]
	(year, month, day, hour, minute, second, microsecond) = (intdata[0], intdata[1], intdata[2], 
															intdata[3], intdata[4], intdata[5], intdata[6])

	time = datetime.datetime(year, month, day, hour, minute, second, microsecond)
	
	return time

raw_out = requests.post("http://challenge.code2040.org/api/time", data=json.dumps(request_payload))

datestamp = eval_r(raw_out.content)["datestamp"]
interval = eval_r(raw_out.content) ["interval"]

print interval, datestamp

time = parse_datestamp(datestamp)

solution = time + timedelta(seconds=interval)

#http://challenge.code2040.org/api/validatetime


payload = {'token': token, 'datestamp': str(solution)}
result = requests.post("http://challenge.code2040.org/api/status", data=json.dumps(payload))

print result.content
