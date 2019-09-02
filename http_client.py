#!/usr/bin/env python3

import socket
import sys

HOST = sys.argv[1]
if( len(sys.argv) < 3):
    PAGE = '/'
else:
    PAGE = sys.argv[2]

print("We will fetch '{0}{1}".format(HOST, PAGE))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,80))

    http_request = "GET {0} HTTP/1.0\r\n\r\n".format(PAGE)

    print("HTTP request:")
    print(http_request)#send request to server
    s.sendall( str.encode( http_request ) )#read all data received from server
    response_buffer = b''

    while True:
        data = s.recv(5566)
        response_buffer += data
        if len(data) == 0:
            break #server closed connection


    print("HTTP response:")#if it's not a utf8 char ignore it
    print(response_buffer.decode('utf-8', "ignore"))