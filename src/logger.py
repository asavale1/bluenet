import sys

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def info(message):
	print HEADER + BOLD + "INFO: " + ENDC + OKBLUE + message + ENDC
	sys.stdout.flush()


def warning(message):
	print HEADER + BOLD + "WARNING: " + ENDC + WARNING + message + ENDC
	sys.stdout.flush()

def error(message):
	print HEADER + BOLD + "ERROR: " + ENDC + FAIL + message + ENDC
	sys.stdout.flush()

def success(message):
	print HEADER + BOLD + "SUCCESS: " + ENDC + OKGREEN + message + ENDC
	sys.stdout.flush()
