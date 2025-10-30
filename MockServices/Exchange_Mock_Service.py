import random
import socket
import string
import threading
import logging
import time
import json

letters = string.ascii_letters + string.digits + string.hexdigits


def generate_random_string(max_len: int):
    rand_len: int = random.randrange(0, max_len, 32)
    return ''.join(random.choice(letters) for i in range(rand_len))


data: str = generate_random_string(10 * 1024)
response_static: str = json.dumps({
    'id': 1, 'data': data
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s",
)


def handle_client(conn, addr):
    """Handle communication with a single client."""
    logging.info(f"New connection from {addr}")
    try:
        with conn:
            data: bytes = conn.recv(1024)
            message: str = data.decode().strip()
            logging.info(f"Received from {addr}: {message}")

            n: int = 0
            while True:
                n = n + 1
                '''response: str = json.dumps({
                    'id': n, 'data': generate_random_string(10 * 1024)
                })'''
                conn.sendall(response_static.encode())
                time.sleep(0.001)
    except Exception as exc:
        logging.info(f'{exc}')


def run_server(host: str, port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    logging.info(f"Server started on {host}:{port}")
    logging.info("Waiting for incoming connections...")

    try:
        while True:
            conn, addr = server.accept()
            thread: threading.Thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            logging.info(f"Active threads: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
    finally:
        server.close()
        logging.info("Server stopped.")


if __name__ == "__main__":
    run_server('0.0.0.0', 52525)
