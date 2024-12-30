import socket
import struct
import random
import string

HOST = '127.0.0.1'
PORT = 65433

def send_message(sock, data_bytes):

    sock.sendall(struct.pack('!I', len(data_bytes)) + data_bytes)

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Підключено до сервера.")

        # Відправимо 100 різних повідомлень
        for i in range(100):
            # Наприклад, змішаємо випадкові числа та випадкові стрінги
            random_number = random.randint(1, 1000)
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            # Формуємо якийсь текст
            message = f"Повідомлення #{i+1} -> num={random_number}, str={random_str}"
            send_message(s, message.encode('utf-8'))

        # Читаємо відповідь від сервера
        raw_length = s.recv(4)
        if raw_length:
            msg_length = struct.unpack('!I', raw_length)[0]
            data = s.recv(msg_length)
            print("Відповідь від сервера:", data.decode('utf-8'))

if __name__ == "__main__":
    run_client()