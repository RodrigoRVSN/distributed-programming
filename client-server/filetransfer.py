from os import path, listdir
import argparse
import socket
import threading

parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='para indicar aplicação como servidora')
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', default=50000)
parser.add_argument('--dir', default='.', help='diretório com arquivos para servir (ignorada se cliente)')
parser.add_argument('--file', default='/', help='arquivo para puxar (ignorada se servidor)')

args = parser.parse_args()

Address = args.host
Port = args.port

# Verificação rapida do argumento
if not path.isdir(args.dir):
    print("Caminho especificado não é um diretório!")
    exit(1)

FileList = '\n'.join(listdir(args.dir))


def handle_client(conn, addr):
    print('Connected by', addr)
    with conn:
        while True:
            data = conn.recv(152)
            if not data: break
            res = bytearray(f'404 Not found\n\n', 'utf-8')
            req = str(data, 'utf-8').split()
            if req[0] == 'GET':
                if req[1] == '/':
                    res = bytearray(f'200 OK\nLenght: {len(FileList)}\n\n{FileList}', 'utf-8')
                else:
                    tmp = path.join(args.dir, req[1])
                    if path.exists(tmp):
                        with open(tmp, 'rb') as f:
                            res = bytearray(f'200 OK\nLenght: {path.getsize(tmp)}\n\n', 'utf-8')
                            data = f.read()
                            res = b''.join([res, data])
            conn.sendall(res)

if args.server:
    print(FileList)  # para feedback, imprime a lista de arquivos da pasta especificada
    with socket.socket() as s:
        s.bind((Address, Port))
        s.listen(5)  # Aumentado para permitir mais conexões pendentes
        print(f"Servidor rodando em {Address}:{Port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr)) # inicia a thread passando os parametros de conexão
            client_thread.start()

else:
    with socket.socket() as s:
        s.connect((Address, Port))
        # Agora uma requisição precisa ser formatada como "GET /arquivo.x\n"
        s.sendall(bytearray('GET {}\n'.format(args.file), 'utf-8'));
        data = s.recv(65535) # Para fins didáticos, não estmos verificando se o arquivo é maior que o buffer (64KB)
        if args.file == '/':
                print(str(data, 'utf-8'))
        else:
            # A resposta deve ser 3 linhas (200 OK) ou 2 linhas (404 Not Found)
            #200 OK\n        |  404 Not Found\n
            #Lenght: 000\n   |  \n
            #\n
            offset1 = data.find(b'\n')  # Primeira linha
            first_line = str(data[:offset1], 'utf-8')
            print(first_line)
            if int(first_line.split()[0]) == 200:
                offset2 = data[offset1+1:].find(b'\n')  # Sedunda linha, cuidado: find está retornando relativo ao offset1
                # Em Python, uma subarray é definida pelas posições absolutas
                offset2 += offset1 + 1
                print(str(data[offset1+1:offset2], 'utf-8'))
                file_size = int(str(data[offset1+1:offset2], 'utf-8').split()[1])
                # Aqui seria feito o tratamento do arquivo recebido após a linha em branco
        s.close()
        
# To handle without threads
""" 
if args.server:
    print(FileList) # para feedback, imprime a lista de arquivos da pasta especificada
    with socket.socket() as s:
        s.bind((Address, Port))
        s.listen(1) 
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(152)
                if not data: break
                res = bytearray(f'404 Not found\n\n', 'utf-8')
                req = str(data, 'utf-8').split()
                if req[0] == 'GET':
                    if req[1] == '/':
                        res = bytearray(f'200 OK\nLenght: {len(FileList)}\n\n{FileList}', 'utf-8')
                    else:
                        tmp = path.join(args.dir, req[1])
                        if path.exists(tmp):
                            with open(tmp, 'rb') as f:
                                res = bytearray(f'200 OK\nLenght: {path.getsize(tmp)}\n\n', 'utf-8')
                                data = f.read()
                                res = b''.join([res, data])
                conn.sendall(res)
"""