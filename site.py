import socket

HOST = '127.0.0.1'
PORT = 6969
filename = "small.png"
with open(filename, 'rb') as f:
    response = f.read()
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            request = data.decode('utf-8')
            conn.send(b'HTTP/1.1 200 OK\r\n')
            conn.send(b'Content-Type: image/jpeg\r\n')
            conn.send(f'Content-Length: {len(response)}\r\n'.encode('utf-8'))
            conn.send(b'Connection: close\r\n')
            conn.send(b'\r\n')
            conn.sendall(response)
            conn.close()