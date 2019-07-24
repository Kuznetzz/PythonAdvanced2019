# Клиент и сервер должны быть реализованы в виде отдельных скриптов,
# содержащих соответствующие функции. Функции клиента: сформировать
# presence-сообщение; отправить сообщение серверу; получить ответ
# сервера; разобрать сообщение сервера; параметры командной строки
# скрипта client.py <addr> [<port>]: addr — ip-адрес сервера; port
# — tcp-порт на сервере, по умолчанию 7777.


import re
import sys
import json
import socket

# parsing arguments

arguments = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1[7777]'
check_spam = [int(i) for i in re.findall(r'\d+', arguments)]

# checking arguments

assert (len(check_spam) == 5), 'Wrong argument formatting. ex: client.py 127.0.0.1[7777]'
assert (all(i < 256 for i in check_spam[:-1])), 'ip must be 0-255.'
assert (1024 < check_spam[-1] < 65536), 'Port number must be 1-65335.'
assert ('.'.join([str(i)for i in check_spam[:-1]])+f'[{check_spam[-1]}]' == arguments),\
        'Letters/symbols inside argument . ex: client.py 127.0.0.1[7777]'

addr = '.'.join([str(i)for i in check_spam[:-1]])
port = check_spam[-1]

print(f'ip-address: {addr}, port: {port}')

# server connecting

try:
    sock = socket.socket()
    sock.connect((addr, port))
    print(f'client was started')

    mess_presence = {"action": "presence",
                    "type": "status",
                    "user": {"account_name":  "Sergey",
                             "status": "Yep, I am here!"}}
    json_mess = json.dumps(mess_presence)

    sock.send(json_mess.encode())
    print(f'client send data: {json_mess}')
    b_response = sock.recv(1024)
    print(f'Server send data: {json.loads(b_response.decode())}')
except KeyboardInterrupt:
    print('Client shutdown. ')


