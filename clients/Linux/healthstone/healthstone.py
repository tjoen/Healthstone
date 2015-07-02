#!/usr/bin/python
# Healthstone System Monitor - (C) 2015 Patrick Lambert - http://healthstone.ca

#
# BEGIN CONFIGURATION
#

# Interval (in seconds) configured in crontab between runs [number]
Interval = 300

# Acceptable CPU threshold [number|False]
CheckCPU = 90

# URL of your Healthstone dashboard [url]
DashboardURL = "http://healthstone.ca/dashboard"

#
# END CONFIGURATION
#

import subprocess
import urllib.request
import urllib.parse

#
# Gather system data
#
hostname = subprocess.check_output(["hostname"]).decode("utf-8").upper().rstrip('\n')
os = subprocess.check_output(["uname", "-srv"]).decode("utf-8").rstrip('\n')
arch = subprocess.check_output(["uname", "-i"]).decode("utf-8").rstrip('\n')
uptime = subprocess.check_output(["uptime"]).decode("utf-8").rstrip('\n')
output = "Healthstone checks: " + hostname + " - " + os + " (" + arch + ")\n\n" + uptime 
(tmp1, tmp2) = uptime.split(': ')
cpu = int(float(tmp2.split(',')[0]))

#
# Run checks
#
alarms = False
if CheckCPU:
	if cpu > CheckCPU:
		alarms = True

#
# Send results off
#
data = "alarms=" + str(alarms) + "&cpu=" + str(cpu) + "&name=" + urllib.parse.quote(hostname, '') + "&output=" + urllib.parse.quote(output, '') + "&interval=" + str(Interval)
result = urllib.request.urlopen(DashboardURL + "/?" + data)