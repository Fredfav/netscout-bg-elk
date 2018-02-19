import os
import sys
from subprocess import check_output, Popen, PIPE, STDOUT
from os import path
import time
import json
from datetime import datetime
from time import strftime

'''
DESCRIPTION
	Script extracting all ASR data from a NETSCOUT InfiniStream
INPUT
	username			username to connect to the InfiniStream
	password			password to connect to the InfiniStream
	interface_number	interface number to extract the data
	ipaddr				IP address of the InfiniStream
	start_time			start date of the data to be extracted (epoch format)
	end_time			end time of the data to be extracted (epoch format)
	filter				filter file name to be used
OUTPUT
	out_folder			output folder where the generated file will be stored
'''

############################## INPUT ##############################

############################## OUTPUT #############################

# Launch the data extraction command
def extract_data(username, password, interface_number, ipaddr, start_time, end_time, filter, out_folder):
#	try:
		command = "/opt/NetScout/dataminingkit/exportclientkit/xdrexport -u " + username
		command += " -p " + password 
		command += " -i " + str(interface_number)
		command += " -a " + ipaddr
		command += " -s " + str(start_time)
		command += " -e " + str(end_time)
		command += " -Q " + filter
		command += " -o " + out_folder
		command += ipaddr + "_"
		command += str(interface_number)
		print command
		p = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
		stdout, stderr = p.communicate()
		print command
		print stdout
		return stdout
#	except: # Catch all exception that exists
#		return 0
		
# Generate all data for all interfaces
def generate_all(username, password, ipaddr, filter, out_folder):
	time = datetime.now().strftime('%s')
	time = int(time) / 300
	end_time = time * 300
	start_time = end_time - 300 # data generation every 5 minutes
	output1 = extract_data(username, password, 3, ipaddr, start_time, end_time, filter, out_folder)
	output2 = extract_data(username, password, 4, ipaddr, start_time, end_time, filter, out_folder)
	output3 = extract_data(username, password, 5, ipaddr, start_time, end_time, filter, out_folder)

	output = output1 + output2 + output3
	return output 

# Main program	
def run(config):
	cfg = json.loads(config)
	username = cfg['username']
	password = cfg['password']
	interface_number = cfg['interface_number']
	ipaddr = cfg['ipaddr']
	filter = cfg['filter']
	out_folder = cfg['out_folder']
	out = generate_all(username, password, ipaddr, filter, out_folder)
	return out
	
# Configuration
config = {
	'username' : 'Administrator',
	'password' : 'netscout1',
	'interface_number' : 3,
	'ipaddr' : '10.10.10.4',
	'filter' : '/opt/NetScout/dataminingkit/exportclientkit/docs/nofilter',
	'out_folder' : '/tmp/export/'
	}
	
results = run(json.dumps(config))
print(results) # verification of the data generation
