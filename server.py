import socket
import argparse
import threading
import ssl
import os



def handleClient (conn, addr):

    print(f"Connected by {addr}")
    print("received:\n")

    while True:

        data = conn.recv(1024)
        if not data:
            break

        print(data.decode())
    
    print("\nEnd of connection\n")
    


os.environ["SSLKEYLOGFILE"] = "sslkeylogfile.txt"



parser = argparse.ArgumentParser()
parser.add_argument("-port", type = int, default = 1313)
parser.add_argument("-key", type = str, default = "key.key")
parser.add_argument("-cert", type = str, default = "crt.crt")
args = parser.parse_args()


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile = args.cert, keyfile = args.key)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(("localhost", args.port))
sock.listen()

ssock = context.wrap_socket(sock, server_side = True)
try:
    
    while True:

        conn, addr = ssock.accept()
        clientThread = threading.Thread(target = handleClient, args = (conn, addr))
        clientThread.start()

except KeyboardInterrupt:

    ssock.close()

    print("End of connection")
