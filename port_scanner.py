#!/usr/bin/env python3

import socket
from termcolor import colored


#shebang python 

def port_scanner(host, port):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Este es nuestro socket AF_INET ya que trabajamos con IPV4 y SOCK_STREAM por usar tcp como conexion
    s.settimeout(1) #EStablecemos el tiempo maximo de comprobacion de 1 segundo, si en un segundo no nos conectamos la conxion no es posible

   #Con connect podemos conectarnos a un host, entablar una conexion y enviar informacion, como solo queremos saber si el puerto esta abierto
   #empleamos connect_ex y trabajamos con el 0  o valor que devuelve, 0 es false y cualquier otro es true pero 0 es que la conexion es exitosa
    if s.connect_ex((host, port)):
        print(colored(f"[!]El puerto {port} esta cerrado", 'red'))
    else:
        print(colored(f"El puerto {port} esta abierto", 'green'))
    s.close()



def main():
    
    host = input(f"\n[+] Introduce la direccion IP: ")
    port = int(input(f"[+] Introduce el puerto a escanear: "))

    port_scanner(host, port)
    



if __name__ == '__main__':
    main()
