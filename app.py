import socket
import threading

# グローバル変数
clients = []

def broadcast(message, sender_socket):
    for client in clients:
        # 送信者にはメッセージを送り返さないようにする
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # クライアントが接続を失った場合、リストから削除
                clients.remove(client)

def handle_client(client_socket):
    # グローバル変数にクライアントを追加
    clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print('メッセージ:', data.decode('utf-8'))

            # 受信したメッセージを全てのクライアントにブロードキャスト
            broadcast(data, client_socket)
        except:
            # エラーが発生した場合、クライアントをリストから削除
            clients.remove(client_socket)
            break

    client_socket.close()

def server():
    server_ip = '0.0.0.0'
    server_port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print('クライアントからの接続を待機中...')

    while True:
        client_socket, client_address = server_socket.accept()
        print('クライアントが接続しました:', client_address)

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def client():
    server_ip = input("サーバーのipアドレス>>")
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print('サーバーに接続しました.')

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

    name = input("名前:")

    while True:
        message = name + ":" + input('クライアントからサーバーに送るメッセージを入力してください: ')
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    print("1:サーバー 2:クライアント")
    user_inp = input(">>")

    if user_inp == "1":
        server()
    elif user_inp == "2":
        client()
    else:
        pass
