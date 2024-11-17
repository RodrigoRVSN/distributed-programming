
import array
import time
import numpy as np

# Gerando 2 vetores com 5 milhões de valores
print('Generating 2 vectors, please wait...', end='', flush=True)
rng = np.random.default_rng()
np_a = rng.integers(-65536, 65536, 5_000_000)
np_b = rng.integers(-65536, 65536, 5_000_000)

# 'q' é uma dica para int32, formato nativo CPython (para ser justo, ~500ms de economia)
a = array.array('q', np_a)
b = array.array('q', np_b)
print(' done.')

def do_computation(name, function):
	print(f'Running {name} computation 20x, please wait...', end='', flush=True)
	elapsed = 0
	for _ in range(20):
		ts = time.process_time_ns()
		dot = function()
		te = time.process_time_ns()
		elapsed += (te - ts)
	print(f' done.\n\t{name} dot {dot}')
	print(f'\t{name} computation total time = {elapsed/1_000_000:.2f}ms')
	print(f'\t{name} computation avg. time = {elapsed/20/1_000_000:.2f}ms')

# Implementação de referência (Gold)
def gold():
	dot = 0
	for i in range(len(a)):
		dot += a[i] * b[i]
	return dot

# Implementação vetorizada
def vectorized():
	return np.dot(np_a, np_b)

# teste de sanidade
do_computation('Gold', gold)
do_computation('Vectorized', vectorized)
print('The dot values must be equal!')
