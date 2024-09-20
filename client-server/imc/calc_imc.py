from concurrent import futures
import argparse
import grpc
import imc_pb2_grpc as imc_grpc
import imc_pb2 as imc_proto


class IMC(imc_grpc.IMC):
    def CalcIMC(self, request, context):
        print(f"received: {request.nome}; {request.peso}; {request.altura}")
        imc = request.peso / (request.altura**2)
        if imc < 18.5:
            notice = "abaixo do peso"
        elif imc < 25.0:
            notice = "saudável"
        elif imc < 30.0:
            notice = "com sobrepeso"
        elif imc < 35.0:
            notice = "obeso"
        elif imc < 40.0:
            notice = "com obesidade severa"
        else:
            notice = "com obesidade morbida"
        return imc_proto.CalcIMCResponse(
            aviso=f"{request.nome} está {notice}", imc=imc
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    imc_grpc.add_IMCServicer_to_server(IMC(), server)
    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("Serving on 127.0.0.1:50051")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action="store_true")
    args = parser.parse_args()
    if args.server:
        try:
            serve()
        except KeyboardInterrupt:
            None
    else:
        channel = grpc.insecure_channel("127.0.0.1:50051")
        client = imc_grpc.IMCStub(channel)
        res = client.CalcIMC(
            imc_proto.CalcIMCRequest(nome="Rodrigo", peso=61, altura=1.64)
        )
        print(f"{res.aviso} ({res.imc :.2f})")
