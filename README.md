# Redes y Sistemas Distribuidos — APIs, sockets y simulación

Trabajos grupales de **Redes y Sistemas Distribuidos (FAMAF–UNC, 2025)**. A partir del respaldo original se identificaron cuatro proyectos:

| Laboratorio | Qué contiene | Tecnologías |
| --- | --- | --- |
| `redes25lab1g35` | API REST de películas: consultas, altas/bajas/cambios y recomendaciones vinculadas con feriados | Python, Flask, Requests, Pytest |
| `redes25lab2g35` | Cliente-servidor para transferencia de archivos sobre TCP, protocolo HFTP y concurrencia con hilos | Python, sockets, threading |
| `redes25lab3g35` | Experimentos de congestión y control de flujo, colas, feedback y pérdidas | C++, OMNeT++, NED |
| `redes25lab4g35` | Evaluación de enrutamiento en una red en anillo, demoras, saltos y ocupación de buffers | C++, OMNeT++, informes y gráficos |

## Cómo se ejecutan (sobre una copia con el código)

**Lab 1:** dentro de la carpeta, instalar dependencias con `python3 -m venv .venv`, activar el entorno, ejecutar `pip install -r requirements.txt` y luego `python main.py`. La API local arranca normalmente en `http://127.0.0.1:5000`; un endpoint es `GET /peliculas`.

**Lab 2:** primero, dentro de `redes25lab2g35/`:

```bash
mkdir -p testdata
python3 server.py --address 127.0.0.1 --port 19500 --datadir testdata
```

En otra terminal, desde la misma carpeta:

```bash
python3 client.py --port 19500 127.0.0.1
```

Esto configura una prueba local, **no** un servicio apto para publicar en Internet.

**Lab 3:** requiere OMNeT++ y las herramientas de compilación del curso. En `redes25lab3g35/`, el proyecto dispone de `network.ned`, `Packet.msg`, `omnetpp.ini` y `Makefile`; normalmente se compila con `make` y se ejecuta con el ejecutable generado (`lab3-kickstarter`) y el archivo `omnetpp.ini`. Puede requerir adaptar Makefile a la versión de OMNeT++.

**Lab 4:** el respaldo conserva fuentes `.cc`, configuraciones, informes y gráficos, **pero faltan `packet.msg` y la definición NED de la red**, necesarias para reconstruir y ejecutar toda la simulación. No se debe presentar como ejecutable sin recuperar esos archivos.

## Estado actual de GitHub

**Las cuatro entradas del repositorio todavía son `gitlinks` y no muestran el código.** El código que permitió identificar estos proyectos está en un ZIP local recuperado, pero aún debe incorporarse al repositorio Git como carpetas versionadas. Por eso las instrucciones de arriba no funcionan sobre un clon vacío del repositorio actual.

No se verificó la ejecución completa de los cuatro laboratorios en el entorno presente.
