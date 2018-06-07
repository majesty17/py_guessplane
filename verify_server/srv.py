#!/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
from time import ctime
import logging

from socket import *


if len(sys.argv)<2:
    print "usage : ./srv.py <datafile>"
    sys.exit(-1)


with open(sys.argv[1]) as file_object:
    lines= file_object.readlines()
    #h=lines[0].strip()
    #map=lines[1].strip()



HOST = ""
PORT = 9000
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)  
tcpSerSock.bind(ADDR)  
tcpSerSock.listen(10)  

print("=====================================================")  
print("waiting to receive messages...")

while True:
    tcpCliSock, addr = tcpSerSock.accept()  
    print("connected from :", addr)  

    data = tcpCliSock.recv(BUFSIZ)  
    if not data:  
        break  
    
    print("received : %s"%data)


    num=int(data[3:])
    map=lines[num*2+1].strip()
    h=lines[num*2].strip()


    ret="0"
    inp1 = data[0]
    inp2 = data[1]
    x = int(inp1)
    y = ord(inp2) - ord('a')
    index=x*10+y

    ret=map[index]

    if data[0:2] in h:
        ret="2"
    
    print "will send : %s"%ret

    
    tcpCliSock.send(ret)  

tcpCliSock.close()  






