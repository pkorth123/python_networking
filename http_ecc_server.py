#!/usr/bin/env python3

import random
import socket
import sys
from task2 import *
from task3_lib import *

PORT = 8080
HOST = '127.0.0.1'

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        my_port = PORT
        while True:
            try:
                s.bind((HOST,PORT))
                break
            except:
                my_port += 1
        s.listen()
        print("Server up and listening on {0}:{1}".format(HOST, PORT))

        while True: #loop forever getting the connection
            print("waiting for the next connection")
            conn, addr = s.accept()
            print("Got a connection from {0}".format(addr))
            try:
                with conn: #python way to close file jhandles automatically
                    process_http_request(conn)
            except Exception as e:
                print("ERROR@@@@ got exception {0}".format(e))

            print("done with connection from {0}".format(addr))


def negotiate_ecc_ssl(conn):
    line = conn.recv(1024)
    line = line.decode('UTF-8', "ignore")
    if line == "HELLO\r\n":
        print("got ECC-ssl hello")
    else:
        raise Exception("ECC-ssl error")
    #send encryption information
    a = 2
    b = 2
    G = (5,1)
    n = 19
    p = 17
    #select random point
    alpha = random.randint(1,n)
    A = k_time_G(G[0], G[1], alpha.n, a, b, p)

    enc_info = "ECC_params: a={0}, b={1}, n={2}, p={}, G1={4}, g2={5}, A1 = {6}, A2 = 7\r\n".format(a,b,n,p,G[0], G[1], A[0], A[1])

    print("Sending ECC-ssl params")
    print(enc_info)
    conn.sendall(str.encode(enc_info)

    #read response with 'B', calculate 'P' and see if test decryption works
	line = conn.recv(1024)
    line = line.decode('UTF-8', "ignore")
    line = line.rstrip('\r\n'))
    ecc_response, params = line.split(': ')
    param_list = params.split(', ')
    ecc_params = ()
    for i in param_list:
        name,value = i.split('=')
        ecc_params[name] = value

    P = k_time_G( ecc_params['B1'], ecc_params[B2], alpha, n, a, b, p)
    enc_key = make_enc_key(P[0], P[1])

    if encrypt( ecc_params["TEST"], dec_key) != "TEST":
        raise Exception("ECC-ssl-error")

    #send "OK" and start encrypting
    conn.sendall(b"OK\r\n")

    return( enc_key, dec_key)


def process_http_request(conn):
    enc_key, dec_key = negotiate_ecc_ssl(conn)
    buff = ''
    while True:
        data = conn.recv(1024)
        if not data:
            break
        buff += data.decode('utf-8', "ignore")
        #check if the request is complete by seeing two returns back to back or a single blank line
        if buff.endswith("\r\n\r\n"):
            break
    #request complete
    print("request:")
    dec_buff = encrypt(buff, dec_key)
    print(dec_buff)
    response = parse_request(dec_buff)

    print(dec_buff)
    response = parse_request(buff)
    if not response:
        response = respond_404('')
    print("response")
    print(response)
    conn.sendall( str.encode(response) )

def parse_request(buff):
    if not request.startswith('GET'):
        return false

    (method, uri, rest) = buff.split(' ',2) #split out the method and uri

    #find the uri on disk
    if uri.endswith('/'):
        uri += 'index.html' #deal with index pages

    filepath = os.getcwd() + uri
    print("Looking for file '{0}'".format(filepath))
    if os.path.isfile( filepath ):
        #FOUND!
        with open(filepath) as fd:
            return make_header( "200 OK", fd.read())
    else:
        print ("Not Found!")
        return False


def respond_404(url):
    html = '''<!DOCTYPE_HTML>
    <HTML><HEAD><TITLE>404 NOt Fount</TITLE></HEAD>
    <BODY>
        <H1>404 Not Found</H1>
        <p>The requested URL was not found on this server.</p>
    </BODY>
    </HTML>
    '''
    return make_header("404 Not Found", html)

def make_header(response_code, payload):
    header = "HTTP/1.0 {0}\r\n".format(response_code)
    header += "Date: {0}\r\n".format( datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') )
    header += "Server: my_python_server\r\n"
    header += "Content-Length: {0}\r\n".format( len(payload) )
    header += "Connetion: close\r\n"
    header += "Content-Type: text/html\r\n"
    header += "\r\n"  #last line super important

    return header + payload





if __name__=="__main__":
    main()