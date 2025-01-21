
import json
import socket

host, port = '0.0.0.0', 52525

if __name__ == '__main__':

    payload: bytes = json.dumps({
        'id': 1, 'side': 'BUY', 'quantity': 10, 'action': 'NEW'
    }).encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        #  sock.bind(('127.0.0.1', 10000))
        bytes_send: int = sock.sendto(payload, (host, port))

        print(f'{bytes_send} bytes_send')
