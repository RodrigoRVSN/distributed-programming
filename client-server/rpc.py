import argparse
import sys
import xmlrpc.client
import xmlrpc.server

parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='para indicar aplicação como servidora')
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', default=50000)

args = parser.parse_args()

Address = args.host
Port = args.port

if args.server:
    with xmlrpc.server.SimpleXMLRPCServer((Address, Port)) as server:
      server.register_introspection_functions()
      server.register_multicall_functions()

      @server.register_function()
      def fn_add(a, b):
        return a + b;

      @server.register_function()
      def fn_sub(a, b):
        return a - b;
        
      @server.register_function()
      def fn_mul(a, b):
        return a * b;
        
      @server.register_function()
      def fn_div(a, b):
        return a / b;
    
      @server.register_function()
      def fn_add_array(arr):
          return sum(arr)

      try:
        server.serve_forever()
      except KeyboardInterrupt:
        sys.Exit(0)

else:
    print(f"Conectado a http://{Address}:{Port}")
    with xmlrpc.client.ServerProxy(f'http://{Address}:{Port}', verbose=True) as proxy:

      # Soma com inteiros
      print("\nSoma com inteiros:")
      result = proxy.fn_add(5, 3)
      print(f"Resultado: {result}")

      # Soma com ponto flutuante
      print("\nSoma com ponto flutuante:")
      result = proxy.fn_add(3.14, 2.86)
      print(f"Resultado: {result}")

      # Soma com arrays
      print("\nSoma com arrays:")
      result = proxy.fn_add_array([1, 2, 3, 4, 5])
      print(f"Resultado: {result}")

      # # Multicall
      # multicall = xmlrpc.client.MultiCall(proxy)
      # multicall.fn_add(2, 3)
      # multicall.fn_div(30, 8)

      # print("Resultados da chamada multicall:")
      # for result in multicall():
      #     print(result)

      # # Multicall
      # multicall = xmlrpc.client.MultiCall(proxy)
      # multicall.fn_add(2, 3)
      # multicall.fn_mul(5, 5)
      # multicall.fn_sub(7, 2)
      # multicall.fn_div(40, 8)

      # print("Resultados da chamada multicall:")
      # for result in multicall():
      #     print(result)

      # # Chamada simples
      # print("\nResultados da chamada simples:")
      # a = proxy.fn_add(2, 3)
      # print(f"a = {a}")
      # b = proxy.fn_mul(a, 2)
      # print(f"b = {b}")
      # c = proxy.fn_sub(b, 5)
      # print(f"c = {c}")
      # d = proxy.fn_div(a, c)
      # print(f"d = {d}")