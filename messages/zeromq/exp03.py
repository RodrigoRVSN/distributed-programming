import argparse
import os
import time
import zmq


def publisher():
    ctx = zmq.Context.instance()
    s: zmq.Socket = ctx.socket(zmq.PUB)
    s.bind("tcp://127.0.0.1:5558")
    print("Crie os clientes em novos terminais e depois [ENTER] aqui ... ")
    input()
    s.send_string("topic_aUma mensagem do topico A")
    s.send(b"topic_b", flags=zmq.SNDMORE)
    s.send_string("Uma mensagem multipart do tópico B")
    time.sleep(1)


def subscriber1():
    ctx = zmq.Context.instance()
    s: zmq.Socket = ctx.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:5558")
    s.subscribe("topic_a")
    try:
        msg = s.recv_string()
        print(f"\n>> Cliente A recebeu: {msg}")
    except KeyboardInterrupt:
        pass


def subscriber2():
    ctx = zmq.Context.instance()
    s: zmq.Socket = ctx.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:5558")
    s.setsockopt(zmq.SUBSCRIBE, b"topic_b")
    try:
        _ = s.recv()  # recebe tópico
        msg = s.recv_string()  # recebe mensagem
        print(f"\n>> Cliente B recebeu: {msg}")
    except KeyboardInterrupt:
        pass


def subscriber3():
    ctx = zmq.Context.instance()
    s: zmq.Socket = ctx.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:5558")
    s.setsockopt(zmq.SUBSCRIBE, b"")
    try:
        print("\n>> Cliente C recebeu: ")
        print(s.recv_string())  # topic_a
        print(s.recv())  # topic_b part 1
        print(s.recv_string())  # topic_b part 2
        print("\n << ---- ")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--client", type=int, choices=range(1, 4))
    args = ap.parse_args()
    if args.client:
        if args.client == 1:
            subscriber1()
        elif args.client == 2:
            subscriber2()
        elif args.client == 3:
            subscriber3()
    else:
        publisher()
