# cliente.py (modelo cliente-servidor)

import sys
import socket
import select
import signal

# Creacion del socket TCP
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def error():
    socket_client.close()
    sys.exit(-1)

def signal_handler(signal, frame):
    socket_client.close()
    sys.exit(0)

def main():
    # CONTROL DE ARGUMENTOS
    if len(sys.argv) != 3:
        print("ERROR: Numero de argumentos incorrecto.")
	print("Uso: python cliente.py [IP_server] [Port_server]")
        error()

    IPserver = sys.argv[1]
    portServer = int(sys.argv[2])
    
    try: # conectamos con el server 
        socket_client.connect((IPserver, portServer))
    except:
        print ("ERROR: no se pudo conectar al servidor")
        error()

    print("Socket enlazado correctamente\n")
    listaSocks = []
    
    print("Introduce un nick: ")
    nick = sys.stdin.readline()

    sys.stdout.write('[Escribe un mensaje] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, socket_client]
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == socket_client:
                # mensaje de otro usuario
                data = sock.recv(4096)
                
                if not data :
                    print '\nDesconectado'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('[Escribe un mensaje] ')
                    sys.stdout.flush()     
            
            else :
                # usuario escribe un mensaje
                msg = sys.stdin.readline()
                socket_client.send(nick+": "+msg)
                sys.stdout.write('[Escribe un mensaje] ') 
                sys.stdout.flush() 
    error()

if __name__ == "__main__":
    main()
