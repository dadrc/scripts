#!/usr/bin/env python2
from threading import Thread
from subprocess import Popen, PIPE
from os import system
from time import sleep
import signal

class Check(Thread):
	def __init__(self, target, command, args, interval):
		super(Check, self).__init__()
		self.target = target
		self.command = command
		self.args = args
		self.interval = interval
		self.daemon = True
	
	def send(self, target, string):
		system("echo \"%s.text = '<span color=\\\"#ffffff\\\">%s </span>'\" | /usr/bin/awesome-client" % (target, string))

	def run(self):
		while True:
			process = Popen([self.command, self.args], stdout=PIPE)
			out, err = process.communicate()
			print out.strip()
			self.send(self.target, out.strip())
			sleep(self.interval)

def interrupt(signal, frame):
	print "Caught interrupt, exiting."

if __name__ == '__main__':
	checks = list()
	checks.append(Check('tempbox', 'monitor-temp', '', 60))
	checks.append(Check('updatebox', 'monitor-updates', '', 30))
	for c in checks:
		c.start()
	# wait for interrupt
	signal.signal(signal.SIGINT, interrupt)
	signal.pause()
