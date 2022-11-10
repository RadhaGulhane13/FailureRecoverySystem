import socket
import time
from threading import Thread

def commit_pid(curr_pid):
    f = open("PID.txt", "w")
    new_pid = str(int(curr_pid) + 1)
    f.write(new_pid)
    
def get_pid():
    f = open("PID.txt", "r")
    curr_pid = f.read();
    f.close()
    return curr_pid

def send_heart_beats_or_pid(conn,address):
    data = conn.recv(1024).decode()
    if (data == "Get Count"):
        curr_pid = get_pid()
        commit_pid(curr_pid)
        conn.send(curr_pid.encode())
    else:
        out = "Healthy State"
        conn.send(out.encode())

def backup_server():
    host = socket.gethostname()
    port = 5018

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    
    loop_inc = 1
    while loop_inc < 100:
        print("waiting for client")
        conn, address = server_socket.accept()
        print("connection has been established")
        t1 =Thread(target = send_heart_beats_or_pid, args = (conn,address))
        t1.start()
        t1.join()
        
        conn.close()  # close the connection
        loop_inc += 1

    
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5018# socket server port number
    
    while True:
        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((host, port))  # connect to the server

            message = "Get Heartbeat" # take input

            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response
            print(data)
            client_socket.close()
            if (data == "Task Accomplished"):
                break
            time.sleep(1)
        except:
            print("Detected Primary Server failure")
            time.sleep(3)
            backup_server()


if __name__ == '__main__':
    client_program()