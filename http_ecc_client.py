#!/usr/bin/env python3

import random
import socket
import sys
import numpy
from task2 import *
from task3_lib import *

HOST = sys.argv[1]
PORT = sys.argv[2]

PAGE = '/'

if( len(sys.argv) < 3):
    PAGE = '/'
else:
    PAGE = sys.argv[2]

print("We will fetch '{0}{1}".format(HOST, PAGE))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))

    #start our ecc-ssl prtocal
    print("Starting ECC-ssl protocal negotiation")
    s.sendall("Hellor\r\n)")
    line = s.recv(1024)
    line = line.decode(('UTF-8', "ignore"))
    print("got: {0}.format(line)")
    if not line.startswith('ECC_params:'):
        raise Exception("ECC-ssl protocal error")

    line = line.rstrip('\r\n')#removenewline
    beginning, param = line.split(': ',1)
    param_list = param.split(', ')
    ecc_params = {}
    for i in param_list:
        name,value = l.split('s')
        ecc_params[name] = value

    #do the ECC encryption to find B
    n = ecc_params['n']
    beta = random.randint(1,n)
    B = k_time_g( ecc_params['G1'], ecc_params['G2'],beta, n, ecc_params['a'],ecc_params['b'], ecc_params['p'])

    #calculate symmetric encryption key "p"
    P = k_time_g( ecc_params),ecc_params['A1'],ecc_params['A2'], beta, n, ecc_params['a'], ecc_params['b'], ecc_params['p'],

    enc_key = make_enc_key(P[0], P[1])
    dec_key = make_dec_key(P[0], P[1])
    test_enc_message = encrypt("TEST", enc_key)

    #send B accross and start encrypting
    enc_response = "ECC_response: B1 = {0}, B2 = {1}, TEST={3}\r\n".format( B[0], B[1], test_enc_message )
    conn.sendall(str.encode(enc_response))

    #wait for serfver to say ok
    line = s.recv(1024)
    line = line.decode('UTF-8', "ignore")
    print("got: {0}".format(line))
    if not line.startswith('OK'):
        raise Exception("ECC-ssl protocol error")


    #continue with http request
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