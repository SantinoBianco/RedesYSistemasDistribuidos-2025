# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode

import os


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.directory = directory
        self.connected = True  # Indica si la conexión sigue activa.
        self.buffer_size = 1024  # Tamaño del buffer para recibir datos.
        print(f"Conexion inicializada con el cliente. Directorio:"
              "{self.directory}")

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        buffer = ""
        try:
            while self.connected:
                data = self.socket.recv(self.buffer_size).decode('ascii')
                # recibe datos del cliente por socket,
                # convierte los binarios an ascii.
                # si el cliente cierra la cone el data es ()"")
                if not data:  # si data es vacio
                    print("Cliente desconectado.")
                    break

                print(f"Datos recibidos del cliente: {data.strip()}")
                buffer += data  # acumula los datos

                # verifica que tenga un comando completo,
                # hasta llegar a un /r/n
                while EOL in buffer:
                    # divide en dos partes el buffer.
                    # command -> primer comando completo(hasta EOL).
                    # buffer -> contiene el resto de datos desp del comando
                    command, buffer = buffer.split(EOL, 1)
                    print(f"Comando recibido: {command.strip()}")
                    if '\n' in command:  # si hay un fin de linea incorrecto
                        self._send_response(f"{BAD_EOL} "
                                            "{error_messages[BAD_EOL]}")
                        buffer = ""  # Limpiar buffer ante error
                        break  # Volver a esperar nuevos datos

                    command = command.strip()  # elimina espacios
                    if command:  # Ignorar líneas vacías
                        self.process_command(command)  # procesa el comand

        except Exception as e:  # cualq  exception
            print(f"Error en la conexión: {e}")
        finally:
            self.socket.close()  # cierra el socket
            print("Conexión cerrada.")

    def process_command(self, command_str):
        """
        Recibe una línea con el comando y sus argumentos, ya validada.
        """
        parts = command_str.split()
        if not parts:
            return

        command = parts[0]

        if command == "get_file_listing":
            self.get_file_listing()
        elif command == "get_metadata":
            if len(parts) == 2:
                self.get_metadata(parts[1])
            else:
                self._send_response(f"{INVALID_ARGUMENTS} "
                                    "{error_messages[INVALID_ARGUMENTS]}")
        elif command == "get_slice":
            if len(parts) == 4 and parts[2].isdigit() and parts[3].isdigit():
                self.get_slice(parts[1], int(parts[2]), int(parts[3]))
            else:
                self._send_response(f"{INVALID_ARGUMENTS} "
                                    "{error_messages[INVALID_ARGUMENTS]}")
        elif command == "quit":
            if len(parts) == 1:
                self.quit()
                self.connected = False
            else:
                self._send_response(f"{INVALID_ARGUMENTS} "
                                    "{error_messages[INVALID_ARGUMENTS]}")
        else:
            self._send_response(f"{INVALID_COMMAND} "
                                "{error_messages[INVALID_COMMAND]}")

    def _send_response(self, message):
        """
        Envia una respuesta al cliente
        """
        self.socket.sendall((message + "\r\n").encode("ascii"))

    def quit(self):
        """
        Manejo del comando quit
        """
        self._send_response(f"{CODE_OK} OK")
        self.connected = False

    def get_file_listing(self):
        """
        Maneja el comando 'get_file_listing'.
        Envía al cliente una lista de archivos en el directorio actual,
        uno por línea, precedido por el código de OK,
        y termina con línea vacía.
        """
        try:
            files = os.listdir(self.directory)
            self._send_response(f"{CODE_OK} OK")
            for fname in files:
                self._send_response(fname)
            self._send_response("")  # Línea vacía para marcar el final
        except Exception as e:
            print(f"Error al obtener la lista de archivos: {e}")
            self._send_response(f"{INTERNAL_ERROR} "
                                "{error_messages[INTERNAL_ERROR]}")

    def get_metadata(self, filename):
        """
        Maneja el comando 'get_metadata'.
        Envía al cliente el tamaño del archivo especificado en bytes.
        """
        try:
            # Construir la ruta completa
            filepath = os.path.join(self.directory, filename)
            print(f"Solicitando metadatos del archivo: {filepath}")

            if not os.path.isfile(filepath):
                print(f"Archivo no encontrado: {filepath}")
                self._send_response(f"{FILE_NOT_FOUND} "
                                    "{error_messages[FILE_NOT_FOUND]}")
                return

            # Obtener el tama;o del archivo
            file_size = os.path.getsize(filepath)
            print(f"Tamaño del archivo '{filename}': {file_size} bytes")
            response = f"{CODE_OK} OK\r\n{file_size}"
            self._send_response(response)
        except Exception as e:
            print(f"Error al obtener metadatos del archivo {filename}: {e}")
            self._send_response(f"{INTERNAL_ERROR} INTERNAL SERVER ERROR")

    def get_slice(self, filename, offset, size):
        """
        Maneja el comando 'get_slice'.
        Envía al cliente un fragmento del archivo especificado,
        codificado en base64.
        """
        try:

            # Construir la ruta completa del archivo
            filepath = os.path.join(self.directory, filename)

            # Verificar si el archivo existe
            if not os.path.isfile(filepath):
                print(f"Archivo no encontrado: {filepath}")
                self._send_response(f"{FILE_NOT_FOUND} "
                                    "{error_messages[FILE_NOT_FOUND]}")
                return
            # Verificar que los parámetros de offset y size sean válidos
            if offset < 0 or size <= 0:
                print(f"Parámetros inválidos: offset={offset}, size={size}")
                self._send_response(f"{INVALID_ARGUMENTS} "
                                    "{error_messages[INVALID_ARGUMENTS]}")
                return

            # Leer el archivo y obtener el fragmento solicitado
            with open(filepath, "rb") as file:
                # Mover el puntero al offset especificado
                file.seek(offset)
                # Leer la cantidad de bytes solicitada
                fragment = file.read(size)

            # Verificar si el fragmento está vacío
            # (offset fuera del tamaño del archivo)
            if not fragment:
                print(f"Offset fuera del tamaño del archivo: offset={offset}")
                self._send_response(f"{BAD_OFFSET} "
                                    "{error_messages[BAD_OFFSET]}")
                return

            # Codificar el fragmento en base64 para enviarlo como texto
            encoded_fragment = b64encode(fragment).decode("ascii")

            self._send_response(f"{CODE_OK} {error_messages[CODE_OK]}")
            self._send_response(encoded_fragment)
        except Exception as e:
            # Manejar errores inesperados
            print(f"Error al procesar get_slice: {e}")
            self._send_response(f"{INTERNAL_ERROR} "
                                "{error_messages[INTERNAL_ERROR]}")
