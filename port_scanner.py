#!/usr/bin/env python3

#Shebang python 

import socket
from termcolor import colored

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
        print(colored(f"[!]El puerto {port} esta cerrado", 'red'))
        s.close()



def main():
    
    host = input(f"\n[+] Introduce la direccion IP: ")
    
    for port in range(1, 1000):
        s = create_socket()
        port_scanner(port,host, s)
    



if __name__ == '__main__':
    main()
