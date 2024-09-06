import argparse
import socket
# ArgParse auxilia interpretar linha de comando facilemnte
parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='suado para inicia a aplicação como servidora')
parser.add_argument('--host', default='localhost', help='nome ou endereço do servidor')
parser.add_argument('--port', type=int, default=50000, help='porta do servidor')
parser.add_argument('--msg', default='Hello World!', help='a mensagem a ser enviada (ignorado se servidor)')
args = parser.parse_args()
Address = args.host
Port = args.port
Msg = args.msg
print(args)

if args.server:
    with socket.socket() as s:
        # Um socket servidor é caracterizado pelas chamadas Bind e Listen
        s.bind((Address, Port)) # os argumentos são uma requisição ao S.O. para  assegurar uma porta permanente nas placas de rede indicadas
        s.listen(1) # o argumento da função é o tamanho da lista de clientes que o     S.O. vai segurar
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(152) # Apenas para fins didáticos, esperamos que o cliente envie uma linha completa
                if not data: break
                rstr = str(data, 'utf-8') # Apenas para fins didáticos, consideramos a requisição como uma string
                conn.sendall(bytearray(rstr.upper(), 'utf-8')) # A conversão é necessária pois sockets transportam bytes por padão
else:
    with socket.socket() as s:
        # Um socket cliente é caracterizado apenas pela chamada Connect, que requisita uma porta e endereço remoto
        s.connect((Address, Port))
        s.sendall(bytearray(Msg[:128], 'utf-8'));
        data = s.recv(152)
        print(str(data, 'utf-8'))
        s.close()

