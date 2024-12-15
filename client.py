import socket
import ssl
import argparse
import os


os.environ["SSLKEYLOGFILE"] = "sslkeylogfile.txt"


parser = argparse.ArgumentParser()
parser.add_argument("-cert", type = str, default = "crt.crt")
parser.add_argument("-port", type = int, default = 1313)
args = parser.parse_args()


sock = socket.create_connection(("localhost", args.port))

context = ssl.create_default_context()
context.load_verify_locations(args.cert)

ssock = context.wrap_socket(sock, server_hostname = "localhost")


try:
    
    while True:

        msg = input()
        ssock.sendall(msg.encode())

except KeyboardInterrupt:

    print("End of connection")