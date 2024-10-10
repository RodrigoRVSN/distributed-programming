import logging
from time import sleep

# Módulo pronto do ZMQ para lidar com looger
from zmq.log.handlers import PUBHandler

# Nossa "aplicação/módulo" (mude o nome para o arquivo que você criou)
import exp04_app as hello

# PUBHandler usa o singleton de contexto e cria o socket
zmq_log_handler = PUBHandler("tcp://127.0.0.1:5555")
# Mudando a formaçao padrao do ZMQ Logger
zmq_log_handler.setFormatter(
    logging.Formatter(fmt="{name} #{lineno:>3} > {message}", style="{")
)
# Todas as mensagens começarao com '{RootTopic}.{level} |', serve para usar como filtro de tópico
zmq_log_handler.setRootTopic("greeter")

# Configuração do Logger do Python
logger = logging.getLogger()  # Root Logger
logger.setLevel(logging.DEBUG)  # maior nivel que pode ser logado
logger.addHandler(zmq_log_handler)  # associa o ZMQ como tratador de mensagens de log

if __name__ == "__main__":
    # ZMQ precisa de oportunidade para rodar e estabelecer conexao
    # ajuste aqui de tal forma que possa ver o log WARNING
    sleep(0.5)
    msg_count = 5
    logger.warning("Preparando modiulos ... ")
    for i in range(1, msg_count + 1):
        logger.debug(f"Enviando mensagem {i} de {msg_count}")
        hello.world()
        sleep(1)
    logger.info("Done!")
