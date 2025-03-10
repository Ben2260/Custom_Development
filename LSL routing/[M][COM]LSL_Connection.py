'''
AUTHOR:     Benjamin Reynolds
UPDATED:    03/09/2025

Title:      [M][COM]LSL_Connection.py

Description:
            This script serves as both an example and a usable substitute
            for connecting any third-party device to the LSL system. I've
            done my best to break down each section of the code along with 
            its purpose and included additional resources in the readme 
            file, so please be sure to review it with that file.
'''


import socket
from pylsl import StreamInfo, StreamOutlet, local_clock
import time
import keyboard

'''
Generate TCP Connection:
    In order to move data from the third-party software to LSL, we needed 
    to connect the third-party output port to an input port over which we 
    have control. This allows us to move data into any other location; in 
    this case, it is LSL. Due to the way this example is set up, we need 
    to run this script after the third-party software has been started. 
'''
host = 'DESKTOP-S8VMNR2'  # Change this to your desired host or IP address
port = 50000        # Choose an available port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections (maximum 5 clients in the queue)
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

# Accept a new connection
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

keyboard.wait('enter')
StartTime = time.time()
print(f"Current Time: {StartTime}")


'''
Generate LSL Connection:
    This script serves as both an example and a usable substitute for 
    connecting any third-party device to the LSL system. I've done my 
    best to break down each section of the code along with its purpose 
    and included additional resources in the readme file, so please be 
    sure to review it with that file.
'''
# Generate LSL object
stream_info = StreamInfo('SimTrigger','EEG',1,100,'float32','sdfwerr32432')
# Connect Unique LSL object to LSL instance
stream_outlet = StreamOutlet(stream_info)

# Test the conection by sending data
cont = -1
stream_outlet.push_sample({cont})

# Wait for 20 seconds so that user can do other things before starting LSL collection.
time.sleep(20)

# Reset count:
cont = 0



'''
Send Data to LSL:
    New data will always be continuously passed from the 3rd party 
    application to this script and then from this program to the instance 
    of LSL. Until ether, the 3rd party application stops sending data or 
    the example of LSL is ended, which will then result in an error, and 
    this program will end.
'''
while True:

    # Receive data from the client
    data = client_socket.recv(1024)  # Adjust buffer size as needed

    # Process the received data (you can customize this part)

    output_numbers = list(data)
    
    fin = output_numbers[0]
    

    if fin == 1:
        cont = cont + 1


        stream_outlet.push_sample({cont})
        CurTime = time.time() - StartTime
        print(f"Current Time: {CurTime}")


    else:
        stream_outlet.push_sample({fin})
    # These are just times when a specific value is read in from the TCP an action is take.
    if cont == 4: 
        break
    elif cont == 3 and  CurTime >= 90:
        break
    #

    

# Close the server socket
server_socket.close()
