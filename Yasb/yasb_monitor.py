#!/usr/bin/env python
import os
import sys
import time

sys.path.append(os.getcwd())

def file_filter(name):
	return (not name.startswith(".")) and (not name.endswith(".swp"))


def file_times(path):
	for file in filter(file_filter, os.listdir(path)):
		yield os.stat(os.path.join(path, file)).st_mtime

def main():
	try:
		import params
		# The path to watch
		path = params.settings["input"]
	except:
		logging.error("Can't import settings in your params.py")
		exit()

	# How often we check the filesystem for changes (in seconds)
	wait = 1

	import Yasb.build

	# The current maximum file modified time under the watched directory
	last_mtime = max(file_times(path))

	while True:
		max_mtime = max(file_times(path))
		if max_mtime > last_mtime:
			last_mtime = max_mtime
			print "Build"
			try:
				Yasb.build.main()
			except:
				pass
		time.sleep(wait)

def main_script():
	try:
		main()
	except Exception, e:
		print e
		pass

if __name__ == "__main__":
	try:
		main()
	except:
		pass