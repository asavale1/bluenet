import re
import subprocess
import logger

WIFI_CONFIG_FILE = "/etc/wpa_supplicant/wpa_supplicant.conf"


def run_command(command):
	return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True).stdout.read()

#def restart_services():
#	subprocess.call(["systemctl","daemon-reload"])
#
#	for service in ["networking"]:
#		command = "/etc/init.d/" + service + " stop; /etc/init.d/" + service + " start"
#		logger.info(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True).stdout.read())
#	#for service in ["ssdp"]:
#	#	command = "systemctl stop " + service + "; systemctl start " + service
#	#	print subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True).stdout.read()
#	#	sys.stdout.flush()

def setup_wifi(wifi_info):
	new_config_info = None
	new_wifi_auth = "network={\n\tssid=\""+ wifi_info["ssid"] +"\"\n\tpsk=\""+ wifi_info["password"] +"\"\n}"

	with open(WIFI_CONFIG_FILE, 'rb') as file:
		old_config_info = file.read()
		
		searchObj = re.search( r'network=\{.*\}', old_config_info, re.M|re.I|re.S)

		if searchObj:
			old_wifi_auth = searchObj.group()
			new_config_info = old_config_info.replace(old_wifi_auth, new_wifi_auth)
		else:
			new_config_info = old_config_info + "\n" + new_wifi_auth + "\n"

	if new_config_info:
		with open(WIFI_CONFIG_FILE, 'wb') as file:
			file.write(new_config_info)

	subprocess.call(["systemctl","daemon-reload"])
	restart()



def power_off():
	logger.info("Shutdown JACK")
	command = "shutdown -h now"
	logger.info(run_command(command))

def restart():
	logger.info("Restart JACK")
	command = "sync; reboot"
	logger.info(run_command(command))

def check_connectivity():
	logger.info("Testing Connectivity")
	find_router_ip = "ip r | grep default | cut -d ' ' -f 3"
	router_ip = run_command(find_router_ip).strip().split("\n")
	if len(router_ip) > 0 : 
		command="ping -q -w 1 -c 1 "+router_ip[0]+" > /dev/null && echo ok || echo error"
		result = run_command(command).strip()
		logger.info(command + "\t=>\t" + result)
		if result == "ok":
			return True
		else:
			return False
	else:
		return False
