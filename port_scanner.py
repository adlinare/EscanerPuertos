#!/usr/bin/env python3

#Shebang python 

import socket
import argparse
from termcolor import colored
import threading

def get_arguments():
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to scan (Ex: 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", required=True, help="Port range to scan (Ex: -p 1-100)")


    option = parser.parse_args()

    return option.target, option.port


#Esta funcion nos permite crear el socket
def create_socket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Este es nuestro socket AF_INET ya que trabajamos con IPV4 y SOCK_STREAM por usar tcp como conexion
    s.settimeout(1) #EStablecemos el tiempo maximo de comprobacion de 1 segundo, si en un segundo no nos conectamos la conxion no es posible
    return s


def port_scanner(port, host):
    
    s = create_socket()
    #Este es otro sistema, empleando connect y viendo si devuelve error de conexion o timeout por espera exesiva 
    try:
        s.connect((host, port))
        print(colored(f"El puerto {port} esta abierto", 'green'))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        s.close()


def scan_ports(ports, target):

    threads = []

    for port in ports:
        thread = threading.Thread(target=port_scanner, args=(port, target))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()



def parse_port(port_str):

    if '-' in port_str:
        start, end = map(int, port_str.split("-"))
        return range(start, end+1)
        
    elif ',' in port_str:
        return map(int, port_str.split(','))

    else:
        return (int(port_str),)


def main():
    
    target, port = get_arguments()
    ports = parse_port(port)
    scan_ports(ports, target)


if __name__ == '__main__':
    main()
