import argparse
import base64

import grpc
import stomp.utils
import imc_pb2_grpc as imc_grpc
import imc_pb2 as imc_proto


import stomp
import stomp.listener
import time


class AdapterListener(stomp.ConnectionListener):
    def __init__(self, conn, channel) -> None:
        self.conn = conn
        self.client = imc_grpc.IMCStub(channel)

    # Quando /queue/imc recebe uma mensagem o broker aciona este metodo
    def on_message(self, frame):
        request = imc_proto.CalcIMCRequest()  # preparação para desserializar obj
        request.ParseFromString(base64.b64decode(frame.body))  # desserializa obj
        tmp = self.client.CalcIMC(request)  # faz a chamada rpc
        response = tmp.SerializeToString()  # serializa a resposta
        self.conn.send(
            destination="/queue/tmp",
            body=base64.b64encode(response),
            content_type="application/octet-stream",
        )  # envia a resposta


class TestListener(stomp.ConnectionListener):
    def on_message(self, frame):
        response = imc_proto.CalcIMCResponse()
        response.ParseFromString(base64.b64decode(frame.body))
        print(f"Recebido: {response.aviso} ({response.imc})")


def adapter(connection):
    channel = grpc.insecure_channel("127.0.0.1:50051")  # Conexão com o gRPC
    connection.set_listener("adapter", AdapterListener(connection, channel))
    connection.connect(wait=True)
    connection.subscribe(destination="/queue/imc", id=int(time.time()))


def tester(connection):
    connection.set_listener("tester", TestListener())
    connection.connect(wait=True)
    connection.subscribe(
        destination="/queue/tmp", id=int(time.time())
    )  # Queue de respostas
    request = imc_proto.CalcIMCRequest(nome="Rodrigo", peso=61, altura=1.64)
    connection.send(
        destination="/queue/imc",
        body=base64.b64encode(request.SerializeToString()),
        content_type="application/octet-stream",
        headers={"reply-to": "/queue/tmp"},
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action="store_true")
    args = parser.parse_args()

    cnn = stomp.Connection()  # Conexao com MQ (localhost:61613)
    cnn.set_listener("prints", stomp.listener.PrintingListener())  # debug
    if args.server:
        adapter(cnn)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            None
    else:
        tester(cnn)
        time.sleep(2)
    cnn.disconnect()
