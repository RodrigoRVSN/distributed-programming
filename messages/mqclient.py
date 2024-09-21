import stomp
import stomp.listener
import time

conn = stomp.Connection()
conn.set_listener("", stomp.listener.PrintingListener())
conn.connect(wait=True)
conn.subscribe(destination='/queue/test', id=int(time.time()))

try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  None

conn.disconnect()