import socket
import time

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5018 # socket server port number
    Restart = False
    
    while True:
        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((host, port))  # connect to the server

            if Restart == True:
                t2 = time.time()
                failure_recovery = t2 - t1
                print(f'*********************FAILURE RECOVERY : {failure_recovery}*******************')
                print(f'*********************IDEAL FAILURE RECOVERY : {failure_recovery - 3}*******************')
                Restart = False

            message = "Get Count" # take input
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response
            print(data)
            client_socket.close()
            if (int(data) == 10):
                print("successfully received 10 PIDs")
                return
            time.sleep(1)
        except:
            print("SERVER CRASH... Trying restart")
            if Restart == False:
                t1 = time.time()
                Restart = True

            

if __name__ == '__main__':
    client_program()