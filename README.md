# Redes y Sistemas Distribuidos — laboratorios (2025)

Repositorio que registra los cuatro laboratorios del **grupo 35** de la materia **Redes y Sistemas Distribuidos (2025)**.

> **Estado actual:** las cuatro entradas del repositorio son **referencias Git a commits externos** (`gitlinks`, modo `160000`), no carpetas con archivos de código. No hay un archivo `.gitmodules` que permita conocer las URLs originales. Por lo tanto, **no es posible ver la implementación de los laboratorios ni ejecutarlos desde este repositorio tal como está**.

## Trabajos registrados

| Entrada | Registro disponible |
| --- | --- |
| `redes25lab1g35` | Referencia al commit del laboratorio 1 |
| `redes25lab2g35` | Referencia al commit del laboratorio 2 |
| `redes25lab3g35` | Referencia al commit del laboratorio 3 |
| `redes25lab4g35` | Referencia al commit del laboratorio 4 |

El nombre del repositorio refleja el área de estudio (**redes y sistemas distribuidos**). Sin el código fuente de las entregas, **no es posible confirmar qué protocolos, herramientas, lenguajes o funcionalidades se implementaron en cada laboratorio**. Para un lector externo es importante distinguir la materia de las implementaciones concretas.

## Cómo consultar los registros Git

Cloná el repositorio y revisá las referencias:

```bash
git clone https://github.com/SantinoBianco/RedesYSistemasDistribuidos-2025.git
cd RedesYSistemasDistribuidos-2025
git ls-tree HEAD
```

Este comando devuelve las entradas de tipo `commit` y sus SHA. **No descarga los trabajos originales.**

En su estado actual, `git submodule update --init --recursive` **no alcanza**, porque falta la configuración `.gitmodules` con las URLs y los caminos de los repositorios vinculados.

## Para completar el portafolio

Una vez recuperadas las ubicaciones originales de los laboratorios:

1. Añadir vínculos directos a los repositorios de origen (si son públicos).
2. Si corresponde, traer el código a directorios versionados o configurar adecuadamente los submódulos.
3. Documentar **por laboratorio** el objetivo, lenguaje, archivos principales, cómo probarlo y resultados observables.

No se incluyen instrucciones genéricas para levantar servidores o clientes de red porque **ninguno de esos comandos puede verificarse contra el código disponible en este repositorio**.

---

**Contexto:** trabajos prácticos académicos de Redes y Sistemas Distribuidos (2025). Este README explica con precisión lo que está disponible y qué falta para que las entregas sean revisables.
