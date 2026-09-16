#!/usr/bin/env python3

#Shebang python 

import socket
import argparse
from termcolor import colored
import sys

def get_arguments():
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", help="Victim target to scan (Ex: 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", help="Port range to scan (Ex: -p 1-100)")


    option = parser.parse_args()

    if option.target is None or option.port is None:
        parser.print_help()
        sys.exit(1)
    return option.target, option.port


#Esta funcion nos permite crear el socket
def create_socket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Este es nuestro socket AF_INET ya que trabajamos con IPV4 y SOCK_STREAM por usar tcp como conexion
    s.settimeout(1) #EStablecemos el tiempo maximo de comprobacion de 1 segundo, si en un segundo no nos conectamos la conxion no es posible
    return s


def port_scanner(port, host, s):
    
    #Este es otro sistema, empleando connect y viendo si devuelve error de conexion o timeout por espera exesiva 
    try:
        s.connect((host, port))
        print(colored(f"El puerto {port} esta abierto", 'green'))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        s.close()



def main():
    
    target, port = get_arguments()

    if '-' in port:
        ports = port.split("-")

        for port in range(int(ports[0]), int(ports[1])):
            s = create_socket()
            port_scanner(port, target, s)

    elif ',' in port:
        ports = port.split(",")
    
        for port in ports:
            s = create_socket()
            port_scanner(int(port), target, s)



        



if __name__ == '__main__':
    main()
