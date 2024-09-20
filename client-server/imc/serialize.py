import imc_pb2 as imc

request = imc.CalcIMCRequest()
request.nome = "Rodrigo"
request.peso = 60
request.altura = 1.64
print(request.SerializeToString())
