#!/usr/bin/env python3
import socket
import sys
from multiprocessing import Process

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    print(f'Getting IP for {host}...')

    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f'Hostname for {host} could not be resolved! Exiting now...')
        sys.exit()

    print(f'IP address of {host} is {remote_ip}')
    return remote_ip


def main():
    host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server...')

        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        while True:
            conn, addr = proxy_start.accept()
            p = Process(target=handle_client, args=(addr, conn))
            p.daemon = True
            p.start()
            print('Started process', p)
            conn.close()


def handle_client(addr, conn):
    print('Connected by', addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


if __name__ == '__main__':
    main()
