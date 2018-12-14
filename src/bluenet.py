#!/bin/python
from bluetooth import *
import json
import signal, sys
import logger, action


CHANNEL = 10
UUID = '94f39d29-7d6d-437d-973b-fba39e49d4ee'

server_sock = None
client_sock = None


def close_connections():
	logger.info("Closing Connections")
	if client_sock:
		client_sock.close()
	if server_sock:
		server_sock.close()
	
	logger.info("**Server Closed**\n\n")

def start_server():
	logger.info("**Server Started**")
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",CHANNEL))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]
	advertise_service( server_sock, "BluenetServer",
									service_id = UUID,
									service_classes = [ UUID, SERIAL_PORT_CLASS ],
									profiles = [ SERIAL_PORT_PROFILE ] )

	logger.info("Waiting for connection on RFCOMM channel %d" % port)

	client_sock, client_info = server_sock.accept()
	logger.success("Accepted connection from " + str(client_info))

	data = None

	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0: break
			logger.info("Received [%s]" % data)
						
			data_json = json.loads(data)
			if(data_json["action"] == "power_off"):
				action.power_off()
			elif(data_json["action"] == "setup_wifi"):
				action.setup_wifi(data_json)
			elif(data_json["action"] == "check_connectivity"):
				client_sock.send(json.dumps({"connectivity": action.check_connectivity()}))
			elif(data_json["action"] == "restart"):
				action.restart()


	except Exception as e:
		logger.error("Exception: " + str(e)) 

	close_connections()

try:
	while True:
		start_server()
except KeyboardInterrupt:
	close_connections()


#
#	Handle Kill Signal
#
def signal_term_handler(signal, frame):
	close_connections()
	sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)
