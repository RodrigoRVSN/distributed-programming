import argparse
import os
import time
import zmq

def printver():
	print(f'Versao da biblioteca nativa: libzmq v{zmq.zmq_version()}')
	print(f'Versao da biblioteca Python: pyzmq v{zmq.__version__}')

def client():
	ctx = zmq.Context()
	socket = ctx.socket(zmq.REQ) # cliente abre a ponta Request
	socket.connect('tcp://127.0.0.1:5555')
	def loop():
		while(True):
			print('Enviando: Hello')
			socket.send_string('Hello')
			msg = socket.recv_string() # recv e bloqueante
			print(f'Recebida: {msg}')
	# Apenas para Windows, para capturar corretamente o CTRL-C
	# é necessário a subproc interrupted e o allow_interrupt
	if os.name == 'nt':
		from zmq.utils.win32 import allow_interrupt
		def interrupted():
			socket.close()
			ctx.destroy()
		with allow_interrupt(interrupted):
			loop()
	else:
		loop()

def server():
	ctx = zmq.Context()
	socket = ctx.socket(zmq.REP) # server abre a ponta Reply
	socket.bind('tcp://127.0.0.1:5555')
	print('Aguardando requisiçao ... ')
	def loop():
		while(True):
			msg = socket.recv_string() # recv e bloqueante
			time.sleep(1)
			print(f'Recebido: {msg}\nRespondendo World!')
			socket.send_string('World')
	# Apenas para Windows, para capturar corretamente o CTRL-C
	# é necessário a subproc interrupted e o allow_interrupt
	if os.name == 'nt':
		from zmq.utils.win32 import allow_interrupt
		def interrupted():
			socket.close()
			ctx.destroy()
		with allow_interrupt(interrupted):
			loop()
	else:
		loop()

if __name__ == '__main__':
	ap = argparse.ArgumentParser(
		description='Apresentacao inicial da biblioteca ZeroMQ\nExemplo Request/Reply',
		epilog='CP117 - FACENS/20204'
	)

	ap.add_argument('-s', '--server', action='store_true', help='roda a aplicacao em modo server')
	args = ap.parse_args()
	printver()
	try:
		if args.server:
			server()
		else:
			client()
	except KeyboardInterrupt:
		pass