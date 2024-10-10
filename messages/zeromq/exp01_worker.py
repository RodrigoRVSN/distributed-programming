

import os
import sys
import time
import zmq

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://127.0.0.1:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://127.0.0.1:5558")

def loop():
	print("Worker ready ... ")
	while True:
		s = receiver.recv()

		# Simple progress indicator for the viewer
		sys.stdout.write('.')
		sys.stdout.flush()

		# Do the work
		time.sleep(int(s)*0.001)

		# Send results to sink
		sender.send(b'')

if os.name == 'nt':
	from zmq.utils.win32 import allow_interrupt
	def interrupted():
		receiver.close()
		sender.close()
		context.destroy()
	with allow_interrupt(interrupted):
		loop()
else:
	loop()