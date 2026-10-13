#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import connection
from constants import *

import threading
import sys


class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))
        # FALTA: Crear socket del servidor, configurarlo, asignarlo
        # a una dirección y puerto, etc.

        # Crea el socket del servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # asignamos dire y puerto al socket
        self.server_socket.bind((addr, port))

        # Guarda el directorio compartido que será utilizado
        # para las operaciones del servidor
        self.directory = directory

        # Configura el socket para escuchar conexiones
        self.server_socket.listen(5)
        print("Servidor escuchando en %s:%s " % (addr, port))

    def handle_client(self, client_socket, client_address):
        """
        Maneja la conexión con un cliente en un hilo separado.
        """
        try:
            print("Conexion aceptada de %s:%s" % client_address)
            # Crea un objeto Connection para manejar la conexión con el cliente
            conn = connection.Connection(client_socket, self.directory)
            print(f"Cliente {client_address} conectado. "
                  "Iniciando manejo de comandos...")
            # Llama al método handle() de la clase Connection
            # para procesar los comandos del cliente
            conn.handle()
        except Exception as e:
            print("Error manejando la conexion con %s:%s: %s" %
                  (client_address[0], client_address[1], e))
        finally:
            client_socket.close()
            print("Conexion cerrada con %s:%s" % client_address)

    def serve(self):
        """
        Loop principal del servidor. Acepta múltiples conexiones
        y las maneja en hilos separados.
        """
        while True:
            try:
                print("Esperando conexiones...")
                # Acepta una conexión entrante
                client_socket, client_address = self.server_socket.accept()
                print(f"Conexión aceptada de {client_address}. "
                      "Creando hilo para manejarla...")
                # Crea un hilo para manejar la conexión con el cliente
                client_thread = threading.Thread(target=self.handle_client,
                                                 args=(client_socket,
                                                       client_address))
                # Inicia el hilo
                client_thread.start()
            except KeyboardInterrupt:
                print("\nServidor detenido manualmente")
                break
            except Exception as e:
                print("Error aceptando conexiones: %s" % e)

        # Cerrar el socket del servidor
        self.server_socket.close()
        print("Servidor cerrado.")


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()