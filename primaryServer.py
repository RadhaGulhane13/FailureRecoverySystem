import sys
import socket
from threading import Thread

local_curr_pid = 0

def init_PID():
    f = open("PID.txt", "w")
    new_PID = str(1)
    f.write(new_PID)
     
def commit_PID(curr_PID):
    f = open("PID.txt", "w")
    new_PID = str(int(curr_PID) + 1)
    f.write(new_PID)
    
def getPID():
    f = open("PID.txt", "r")
    curr_PID = f.read();
    f.close()
    global local_curr_pid
    local_curr_pid = int(curr_PID)
    return curr_PID

def send_heart_beats(conn, address):
    data = conn.recv(1024).decode()
    if (data == "Get Count"):
        curr_PID = getPID()
        commit_PID(curr_PID)
        conn.send(curr_PID.encode())
    else:
        out = "Healthy"
        conn.send(out.encode())
    
def server_program(testcase):
    host = socket.gethostname()
    port = 5018

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))
    server_socket.listen()
    print("server is listning")
    #count = 1
    loop_inc = 1
    while loop_inc < 100: 
        print("waiting for client")   
        conn, address = server_socket.accept()

        global local_curr_pid
        print("connection has been established")

        if (testcase == "testcase1"):
            #stop after 10 PIDs
            if local_curr_pid == 10:
                out = "Task Accomplished"
                conn.send(out.encode())
                conn.close()
                break
        elif (testcase == "testcase2" and loop_inc == 7):
            #stop randomly
            if (loop_inc == 7):
                conn.close()
                print("Server CRASH")
                break
        
        t1 =Thread(target = send_heart_beats, args = (conn, address))
        t1.start()
        t1.join()
        
        conn.close()  # close the connection
        loop_inc += 1
        

if __name__ == '__main__':
    testcase = sys.argv[1]
    init_PID()
    server_program(testcase)
    
