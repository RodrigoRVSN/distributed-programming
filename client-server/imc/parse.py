import imc_pb2 as imc

data = b'\n\x07Rodrigo\x11\x00\x00\x00\x00\x00\x00N@\x19=\n\xd7\xa3p=\xfa?'
request = imc.CalcIMCRequest()
request.ParseFromString(data)
print(f'Nome: {request.nome}')
print(f'Peso: {request.peso}')
print(f'Altura: {request.altura}')