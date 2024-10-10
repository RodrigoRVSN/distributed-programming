import os
import zmq
import random
import time

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://127.0.0.1:5557")

# Socket with direct access to the sink: used to synchronize start of batch
sink = context.socket(zmq.PUSH)
sink.connect("tcp://127.0.0.1:5558")

print("Press Enter when the workers are ready: ")
_ = input()
print("Sending tasks to workers ... ")

def main():
	try:
		sink.send(b'0')

		# Initialize random number generator
		random.seed()

		# Send 100 tasks
		total_msec = 0
		for _ in range(100):
			# Random workload from 1 to 100 msecs
			workload = random.randint(1, 100)
			total_msec += workload
			sender.send_string(f"{workload}")

		print(f"Total expected cost: {total_msec} msec")
	except KeyboardInterrupt:
		pass

if os.name == 'nt':
  from zmq.utils.win32 import allow_interrupt
  def interrupted():
    sender.close()
    sink.close()
    context.destroy()
  with allow_interrupt(interrupted):
    main()
else:
  main()

# Give OMQ time to deliver
time.sleep(1)