#!/usr/bin/env python3
############################################################
#
# MIT License
#
# Copyright (c) 2017 Hilscher Systemautomation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
############################################################

import profinet.dcp
import profinet.util
import json
import iothub_client
from iothub_client import IoTHubClient, IoTHubTransportProvider
from iothub_client import IoTHubMessage
import os

### IotHub options
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
CONNECTION_STRING = os.environ['IOTHUB_CONNECTION_STRING']

### scan options
ethIf = 'cifx0'
scanTimeout = 10
verbose = True

### iot hub utility functions
def sendConfirmationCallback(message, result, user_context):
	verbose and print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )

def iothubClientInit():
	# prepare iothub client
	client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
	# set the time until a message times out
	client.set_option("messageTimeout", MESSAGE_TIMEOUT)
	client.set_option("logtrace", 0)
	return client

### main

# open network interface for device scan
rawSocket = profinet.util.ethernet_socket(ethIf, 3)
srcMac = profinet.util.get_mac(ethIf)

# open connection to cloud
verbose and print('Connecting to Azure IotHub...')
client = iothubClientInit()
messageCounter = 0

# cyclically scan network
while True:
	# discover profinet devices
	verbose and print('Discovering PROFINET devices...')
	profinet.dcp.send_discover(rawSocket, srcMac)
	rawDeviceList = profinet.dcp.read_response(rawSocket, srcMac, to=scanTimeout, debug=verbose)

	# prepare JSON message
	jsonList = []
	for devMac in rawDeviceList.keys():
		jsonList.append({'deviceType': 'profinet',
	                         'macAddress': profinet.util.mac2s(devMac),
	                         'nameOfStation': profinet.util.decode_bytes(rawDeviceList[devMac]['name']),
	                         'ipAddress': rawDeviceList[devMac]['ip'],
	                         'vendorId': (rawDeviceList[devMac]['devId'][0] << 8) + rawDeviceList[devMac]['devId'][1],
	                         'deviceId': (rawDeviceList[devMac]['devId'][2] << 8) + rawDeviceList[devMac]['devId'][3]
	                        })
	jsonMessage = json.dumps(jsonList)
	verbose and print(jsonMessage)

	message = IoTHubMessage(jsonMessage)

	# sending device list to cloud service
	verbose and print('Sending device list to IotHub...')
	client.send_event_async(message, sendConfirmationCallback, messageCounter)
	messageCounter += 1
