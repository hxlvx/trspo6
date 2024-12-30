import socket
import struct

HOST = '127.0.0.1'
PORT = 65433

def receive_message(conn):
    # Спочатку зчитаємо 4 байти довжини
    raw_length = conn.recv(4)
    if not raw_length:
        return None

    # Перетворюємо отримані 4 байти на число (little-endian чи big-endian – дивіться самі)
    msg_length = struct.unpack('!I', raw_length)[0]

    # Зчитаємо решту даних
    data = b''
    while len(data) < msg_length:
        packet = conn.recv(msg_length - len(data))
        if not packet:
            return None
        data += packet
    return data

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер слухає на порту {PORT}...")

        conn, addr = s.accept()
        with conn:
            print(f"Підключився клієнт: {addr}")

            # Отримуємо 100 повідомлень
            for i in range(100):
                data = receive_message(conn)
                if not data:
                    print("З'єднання закрито клієнтом передчасно.")
                    break
                print(f"Повідомлення #{i+1}: {data.decode('utf-8')}")

            # Для прикладу: відправимо 1 повідомлення назад
            response_text = "Сервер отримав ваші 100 повідомлень!"
            encoded = response_text.encode('utf-8')
            # Упаковуємо довжину
            conn.sendall(struct.pack('!I', len(encoded)) + encoded)

if __name__ == "__main__":
    run_server()