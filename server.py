import socket
from _thread import *
import pickle

package_size = 2048 * 8

server = "192.168.0.154"
# Change server to own ip address as well as in network.py to run
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))


s.listen(6)
print("Waiting for connection, Server Started")

# RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
MAGENTA = (255, 0, 255)

Colors = [RED, GREEN, BLUE, YELLOW, AQUA, MAGENTA]


def threaded_client(conn, playerColor):
    print("sending color: " + str(playerColor))
    conn.send(pickle.dumps(playerColor))
    print("color sent")
    reply = " "
    while True:
        try:
            # print("receiving data")
            data = pickle.loads(conn.recv(package_size))
            # get rect from client and change on server
            players.update({playerColor: data})

            data = players

            if not data:
                print("Disconnected")
                players.pop(playerColor)
                Colors.append(playerColor)
                break
            else:
                reply = players

                print("Received: " + str(data))
                print("Sending: " + str(reply))

            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print("error:" + str(e))
            break

    print("Lost Connection")
    players.pop(playerColor)
    Colors.append(playerColor)
    conn.close()


players = {}
while True:
    try:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, Colors.pop()))
    except Exception as e:
        print("Can't connect. Too many players joined")
        print(e.__class__)
