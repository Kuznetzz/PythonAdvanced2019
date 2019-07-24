# Функции сервера: принимает сообщение клиента; формирует ответ клиенту; отправляет
# ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт для работы
# (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию
# слушает все доступные адреса).

import re
from argparse import ArgumentParser
import socket
import json

# parsing  arguments
parser = ArgumentParser()

parser.add_argument(
    '-p', '--port', type=int,
    required=False, help='Port Number', default=7777)

parser.add_argument(
    '-a', '--addr', type=str,
    required=False, help='ip-address', default='0.0.0.0')

args = parser.parse_args()

assert ([0 <= int(x) < 256 for x in re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', args.addr).
                                             group(0))].count(True) == 4), 'wrong ip'
assert (1024 < args.port < 65536), 'wrong port'

addr, port = args.addr, args.port

# server working
try:
    sock = socket.socket()
    sock.bind((addr, port))
    sock.listen(5)
    print(f'server started with { addr }:{ port }')

    while True:
        client, address = sock.accept()
        print(f'client was detected {address[0]}:{address[1]}')

        b_request = client.recv(1024)
        payload_client = json.loads(b_request.decode())
        print(f'Client {payload_client["user"]["account_name"],}',
              f'status: {payload_client["user"]["status"]}')

        if payload_client["action"] == 'presence':
            b_responce = {"response": 200,
                          "alert":"presence done"}
        else:
            b_responce = {"response": 400,
                          "alert": "wrong json procedure"}

        payload_server = json.dumps(b_responce)
        print(f'Server send data:{payload_server}')
        client.send(payload_server.encode())
        client.close()

except KeyboardInterrupt:
    print('Server shutdown. ')


