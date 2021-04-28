#!/usr/bin/env python3
            
import socket
import json
import hashlib
import os.path
from aes import AESCipher

def verifyAES(encypted_message, original_message):

    key = 'ASD120KLO12OQN39'
    aes = AESCipher(key)
    message = aes.decrypt(encypted_message)
    
    if original_message.decode("utf-8")  == message:
        return 1
        
    return 0

def verifyCredentials(credentials):

    utf_encoded = credentials['password'].encode('utf-8')
    hashed = hashlib.sha512(utf_encoded).hexdigest()
    
    filename = credentials['username']+'.txt'
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
           data = json.load(file)
    else:
        return 'User not found!' 
       
    if hashed == data['password']:
        return 'Verification Successful!'
        
    return 'Incorrect Password!'

def registerCredentials(credentials):

    utf_encoded = credentials['password'].encode('utf-8')
    hashed = hashlib.sha512(utf_encoded).hexdigest()

    to_write = {'password': hashed}
    filename = credentials['username']+'.txt'
    
    if os.path.exists(filename):
        return b'Username Exists Already!'   
        
    else:
        with open(filename, 'w') as file:
           file.write(json.dumps(to_write))
           
    return b'Registration Successful!'


if __name__ == '__main__':

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 9999
    buffer_size = 4096
    serverSocket.bind((host, port))
    serverSocket.listen(10)

    print("Listening on %s:%s..." % (host, str(port)))

    while True:
    
        clientSocket, address = serverSocket.accept()
        data = clientSocket.recv(buffer_size)
        credentials = json.loads(data.decode('utf-8'))
        
        if len(credentials) == 2:
        
            print("Verification Request Received from %s..." % str(address))
            
            verified = verifyCredentials(credentials)
            clientSocket.send(bytes(str(verified), 'utf-8'))
                
        else:
        
            print("Registration Request Received from %s..." % str(address))
            
            original_message = b'Message-to-Encrypt'
            clientSocket.send(original_message)
            encypted_message = clientSocket.recv(buffer_size)

            auth = verifyAES(encypted_message, original_message)
            
            if auth:
                status = registerCredentials(credentials)
                clientSocket.send(status)
                
            else:
                clientSocket.send(b'Authentication Failure')
                
        clientSocket.close()