#!/usr/bin/env python3

#Shebang python 

import socket
import argparse
import signal
import sys
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor #Esta clase nos permite limitar la  pool de ejecuon para no desbordar los hilos

open_sockets = []

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...", 'red'))
    for socket in open_sockets:
        socket.close()

    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)# Ctrl + c

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
    
    open_sockets.append(s)

    return s


def port_scanner(port, host):
    
    s = create_socket()
    #Este es otro sistema, empleando connect y viendo si devuelve error de conexion o timeout por espera exesiva 
    try:

        s.connect((host, port))
        #Nos quedamos con las cabeceras para saber ante que servicio nos encontramos
        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        response = s.recv(1024).decode(errors='ignore').split('\n')

        if response:
            print(colored(f"\n[+] El puerto {port} esta abierto\n",'green'))
            for lines in response:
                print(colored(f"{lines}", 'grey'))
        else:
            print(colored(f"[+]El puerto {port} esta abierto", 'green'))
    except (socket.timeout, ConnectionRefusedError):
        pass 
    finally:
        s.close()


def scan_ports(ports, target):

    #max_workers es el numero maximo de la pool
    with ThreadPoolExecutor(max_workers=600) as executor:
        executor.map(lambda port: port_scanner(port, target), ports)

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
