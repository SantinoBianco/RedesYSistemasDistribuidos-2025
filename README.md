# Redes y Sistemas Distribuidos — APIs, sockets y simulación

Cuatro laboratorios grupales de **Redes y Sistemas Distribuidos (FAMAF – UNC, 2025)**. El repositorio contiene el código y material de apoyo de los **cuatro proyectos**, organizados en carpetas que se pueden consultar directamente desde GitHub.

| Laboratorio | Proyecto | Tecnologías |
| --- | --- | --- |
| [Lab 1](./redes25lab1g35) | API REST de películas y recomendaciones relacionadas con feriados | Python, Flask, Requests, Pytest |
| [Lab 2](./redes25lab2g35) | Cliente-servidor de transferencia de archivos mediante TCP y protocolo HFTP | Python, sockets, hilos |
| [Lab 3](./redes25lab3g35) | Simulaciones de congestión, control de flujo, buffers y pérdidas de paquetes | C++, OMNeT++, NED |
| [Lab 4](./redes25lab4g35) | Simulación y análisis del enrutamiento de una red en anillo, demoras y cantidad de saltos | C++, OMNeT++, gráficos e informes |

## Clonar y explorar

```bash
git clone https://github.com/SantinoBianco/RedesYSistemasDistribuidos-2025.git
cd RedesYSistemasDistribuidos-2025
```

### Lab 1 — API REST con Flask

En Linux, desde la carpeta `redes25lab1g35/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

La API se inicia generalmente en `http://127.0.0.1:5000`; entre sus endpoints está `GET /peliculas`.

[Video de presentación del laboratorio](https://www.youtube.com/watch?v=KnnIzNtJSQQ).

### Lab 2 — Transferencia de archivos con sockets TCP

Usá **dos terminales**. Desde `redes25lab2g35/`, iniciá el servidor:

```bash
mkdir -p testdata
python3 server.py --address 127.0.0.1 --port 19500 --datadir testdata
```

En la segunda terminal, en la misma carpeta:

```bash
python3 client.py --port 19500 127.0.0.1
```

Esta es una demostración **local**, no un servicio endurecido para exposición pública. [Video de presentación](https://www.youtube.com/watch?v=xKkGWOj-lbI).

### Lab 3 — Congestión y control de flujo

Requiere **OMNeT++** con herramientas de compilación compatibles. La carpeta contiene `network.ned`, `Packet.msg`, `omnetpp.ini`, código `.cc`, `Makefile` y [un informe de experimentos](./redes25lab3g35/Informe.md).

```bash
cd redes25lab3g35
make
```

El binario y su ejecución dependen de la versión instalada de OMNeT++; consultá las configuraciones del laboratorio.

### Lab 4 — Enrutamiento y métricas

Incluye código C++ para simulaciones, resultados y [gráficos de análisis](./redes25lab4g35/graficos). **Limitación del respaldo:** faltan una definición NED de la topología y `packet.msg`, necesarios para reconstruir la ejecución íntegra del laboratorio en OMNeT++. El material publicado **sí permite revisar su implementación y resultados**, aunque no ejecutar todo de principio a fin sin recuperar esos archivos.

## Contenidos trabajados

- **Diseño de APIs** y comunicación HTTP.
- **Programación de redes con sockets TCP** y concurrencia.
- **Simulación discreta** de tráfico, colas y congestión.
- **Análisis de métricas de redes** a partir de experimentos.

**Estado:** los cuatro laboratorios están publicados como carpetas Git normales, no como enlaces vacíos a otros commits. Las instrucciones no se han verificado mediante una ejecución completa de todos los proyectos.
