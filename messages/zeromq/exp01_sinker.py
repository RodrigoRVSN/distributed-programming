import os
import sys
import time
import zmq

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://127.0.0.1:5558")

def main():
	print("Sink waiting batch ... ")
	try:
		# Wait for start of batch
		_ = receiver.recv()

		# Start our clock now
		tstart = time.time()

		# Process 100 confirmations
		for task_nbr in range(100):
			_ = receiver.recv()
			if task_nbr % 10 == 0:
				sys.stdout.write(':')
			else:
				sys.stdout.write('.')
			sys.stdout.flush()

		# Calculate and report duration of batch
		tend = time.time()
		print(f"\nTotal elapsed time: {(tend-tstart)*1000} msec")
	except KeyboardInterrupt:
		pass

if os.name == 'nt':
	def interrupted():
		receiver.close()
		context.destroy()
	from zmq.utils.win32 import allow_interrupt
	with allow_interrupt(interrupted):
		main()
else:
	main()