# Informe Laboratorio 3 - Modelo De Anillo 
**REDES Y SISTEMAS DISTRIBUIDOS**
# INTEGRANTES

- __Fabrizio Luciano Reyna,__
- __Luis Bautista Cordoba buffa,__
- __Santino Bianco Monasterio,__ 
- __Facundo Gabriel Garione Chavez__

## RESUMEN

En este trabajo analizamos el comportamiento de una red en anillo simulada en OMNeT++, bajo diferentes estrategias de enrutamiento. Medimos métricas clave como delay, hop count y utilización de buffers. Finalmente, diseñamos una mejora de enrutamiento y comparamos resultados.

## INTRODUCCIÓN
La simulación discreta nos permite modelar redes de computadoras y observar su comportamiento en distintos escenarios. Utilizamos OMNeT++ para evaluar un sistema de enrutamiento en una red con topología en anillo, analizando cómo el tráfico es gestionado por los nodos y cómo se ven afectados los recursos como enlaces y buffers.

## TAREA ANÁLISIS:

El presente trabajo práctico tiene como objetivo el análisis del rendimiento de un sistema de enrutamiento en red mediante el uso del simulador OMNeT++. Para ello, los profesores nos dieron un modelo de red provisto, el cual nosotros vamos a analizar con estadísticas que agregaremos para que nos permitan estudiar las diferentes métricas de desempeño de esta red.

En este laboratorio los profesores nos dieron dos casos para que los analicemos:

__Caso 1:__ Nosotros deberemos correr el modelo con las fuentes de tráfico configuradas y estudiaremos las métricas tomadas que nos devolvieron.

__Caso 2:__ Asumimos que todos los nodos (0,1,2,3,4,6,7) generan tráfico hacia el
node[5] con packetByteSize e interArrivalTime idénticos entre todos los nodos. Determinaremos a partir de que valor de interArrivalTime se puede garantizar un equilibrio o estabilidad en la red.


### OBJETIVOS PRINCIPALES:

Incluir métricas de análisis que permitan evaluar el comportamiento de la red bajo distintas condiciones de tráfico. Entre las estadísticas recomendadas se encuentran:
- Demora de entrega de los paquetes (delay).
- Cantidad de saltos (hops) que realiza cada paquete hasta su destino.
- Utilización de los buffers en cada nodo intermedio.
- Uso de los enlaces de comunicación, evaluando si están saturados o infrautilizados.
- Pérdidas de paquetes, si es que las hubiera.

## EXPERIMENTO CASO 1:
| Buffer| delay | HopCount |
| ------ | ------ | ------ |
|![](graficos/BufferSizeParte1-Caso1(1).png)|![](graficos/DelayParte1-caso1(1).png)|![](graficos/HopCountParte1-Caso1(1).png)|
|![](graficos/BufferSizeParte1-Caso1(0.5).png)|![](graficos/DelayParte1-Caso1(0.5).png)|![](graficos/HopCountParte1-Caso1(0.5).png)|
|![](graficos/BufferSizeParte1-Caso1(0.1).png)|![](graficos/Delay-parte1-caso1(0.1).png)|![](graficos/HopCount-parte1-caso1(0.1).png)|

#### PREGUNTAS A RESPONDER:
__1. ¿Qué métricas se obtienen?__ 

Las métricas obtenidas en el experimento son las siguientes:

- BufferSize (Tamaño del buffer):

Representa la cantidad de paquetes acumulados en el buffer de cada nodo.
Ejemplo:
Network.node[0].lnk[0]: Tamaño promedio del buffer es 92.92, indicando congestión en este nodo.
Network.node[2].lnk[0]: Tamaño promedio del buffer es 3.29, indicando que este nodo está menos cargado.
Otros nodos (node[7], node[1], node[6]) tienen buffers pequeños (0.5), lo que indica que están procesando los paquetes rápidamente.

- LinkUtilization (Utilización del enlace):

Representa la cantidad de veces que un enlace es utilizado para enviar paquetes.
Ejemplo:
Todos los enlaces tienen una utilización promedio de 1, lo que indica que están completamente utilizados durante la simulación.

- Delay (Demora):

Representa el tiempo promedio que tardan los paquetes en llegar a su destino.
Ejemplo:
Network.node[5].app: Demora promedio es 51.16 segundos, con una desviación estándar alta (28.37), indicando variabilidad en los tiempos de entrega.

- HopCount (Número de saltos):

Representa la cantidad de nodos que un paquete atraviesa antes de llegar a su destino.
Ejemplo:
Network.node[5].app: Número promedio de saltos es 3.92, con una desviación estándar baja (0.99), indicando que la mayoría de los paquetes siguen rutas similares.


__2. ¿Cómo es el uso de los recursos de la red?__ 
[!imagenes graficos]
El uso de los recursos de la red se puede analizar en términos de buffers, enlaces y nodos:

- Buffers:

El nodo node[0] tiene un tamaño promedio de buffer alto (92.92), lo que indica que está recibiendo más tráfico del que puede procesar, causando congestión.
Otros nodos (node[2], node[7], node[1], node[6]) tienen buffers pequeños (0.5 o 3.29), lo que indica que están funcionando eficientemente y no están acumulando tráfico.

- Enlaces:

Todos los enlaces tienen una utilización promedio de 1, lo que indica que están completamente utilizados durante la simulación. Esto sugiere que la red está operando en su capacidad máxima, lo que podría explicar las demoras altas.

- Nodos:

El nodo node[5] tiene una demora promedio alta (51.16 segundos), lo que indica que los paquetes tardan mucho en llegar a su destino.
Esto podría deberse a congestión en la red o a rutas largas para los paquetes.

__3. ¿Se puede mejorar?__

Sí se puede mejorar de varias maneras:

- Aumentado la capacidad de los enlaces, incrementando el ancho de banda de los enlaces para reducir la congestión y mejorar el rendimiento

- Optimizando el enrutamiento mediante un algoritmo de enrutamiento bidireccional para reducir el numero de saltos y la demora, permitiendo que los paquetes tomen rutas mas cortas y eviten congestion de ciertos nodos

- Distribuyendo el tráfico con mas nodos para generar tráfico hacia node[5] con tasas de generacion ajustadas equilibrando la carga entre los nodos y reduciendo la congestión en el node[0]

## EXPERIMENTO CASO 2:
| Buffer| delay | HopCount |
| ------ | ------ | ------ |
|![](graficos/BufferSizeParte1-Caso2(1).png)|![](graficos/DelayParte1-Caso2(1).png)|![](graficos/HopCountParte1-Caso2(1).png)|
|![](graficos/BufferSizeParte1-Caso2(0.5).png)|![](graficos/DelayParte1-Caso2(0.5).png)|![](graficos/HopCountParte1-Caso2(0.5).png)|
|![](graficos/BufferSizeParte1-Caso2(0.1).png)|![](graficos/DelayParte1-Caso2(0.1).png)|![](graficos/HopCountParte1-Caso2(0.1).png)|


Para garantizar un equilibrio o estabilidad en la red, se debe analizar el comportamiento de las métricas clave en función del valor de interArrivalTime. 

1. Analisis de los resultados:

- Con interArrivalTime = 0.1:

BufferSize: Están altamente congestionados, con valores promedio a 1000 paquetes en la mayoría de los nodos. Esto indica que la red no puede procesar el tráfico generado.

Delay: La demora promedio es alta (90.40 segundos), lo que refleja una red saturada.

HopCount: El número de saltos promedio es bajo (1.11), pero esto se debe a que los paquetes no están siendo procesados eficientemente.

- Con interArrivalTime = 0.5:

BufferSize: Están menos congestionados, con valores promedio entre 100 y 200 paquetes, indica una mejora en la capacidad de procesamiento de la red.

Delay: La demora promedio disminuye a 73.19 segundos, pero sigue siendo alta.

HopCount: El número de saltos promedio aumenta a 1.54, refleja un mejor enrutamiento.

- Con interArrivalTime = 1:

BufferSize: Están casi vacíos, con valores promedio cercanos a 100 paquetes o menos en la mayoría de los nodos, esto indica que la red está procesando el tráfico de manera eficiente.

Delay: La demora promedio disminuye significativamente a 64.53 segundos, lo que refleja una red más estable.

HopCount: El número de saltos promedio aumenta a 2.06, lo que indica que los paquetes están tomando rutas más largas pero eficientes.

2. Determinación del equilibrio:

El equilibrio o estabilidad analizando todos los casos vimos que a partir de interArrivalTime = 1 es el mas conveniente, porque permite un procesamiento eficiente del tráfico generado por todos los nodos hacia node[5], evitando congestión y manteniendo un uso óptimo de los recursos.


## TAREA DE DISEÑO
### DISEÑO
Para superar las limitaciones de la estrategia original (que siempre reenvía en sentido horario), diseñamos una estrategia semiestática basada en el índice del nodo actual y su proximidad al nodo destino.

Analizamos la topología fija de anillo con 8 nodos, y establecimos reglas por nodo para enviar en la dirección más corta hacia el nodo destino (node[5]) sin requerir mensajes hello ni tablas de ruteo.
### LOGICA IMPLEMENTADA
- Nodos 0, 6 y 7: reenvían siempre en sentido horario (toLnk[0]).

- Nodos 2, 3 y 4: reenvían siempre en sentido antihorario (toLnk[1]).

- Nodo 1: alterna entre ambas interfaces en cada reenvío para balancear la carga.

- Nodo 5: es el destino, por lo que recibe los paquetes y no reenvía.

- Nodo desconocido o fuera de rango: (no sucede en esta topología), usaría gate 0 como fallback.
### CODIGO BASE
~~~
int gateIndex = 0;

if (myIndex == 0 || myIndex == 6 || myIndex == 7) {
    gateIndex = 0;
}
else if (myIndex == 2 || myIndex == 3 || myIndex == 4) {
    gateIndex = 1;
}
else if (myIndex == 1) {
    gateIndex = toggleGate;
    toggleGate = 1 - toggleGate;
}

pkt->setHopCount(pkt->getHopCount() + 1);
send(msg, "toLnk$o", gateIndex);

~~~
### OBJETIVOS DE ESTA ESTRATEGIA
- Reducir el número de saltos.

- Evitar acumulación en nodos como node[0].

- Balancear la carga de tráfico entre caminos alternativos.

- No depender de funciones especiales de OMNeT++ como cTopology.
### RESULTADOS CASO 1
        En el HopCount son saltos constantes de 3 nodos.
        
| Buffer| delay |
| ------ | ------ |
|![](graficos/BufferSize-caso1-parte2(1).png)|![](graficos/delay-parte2-caso1(1).png)|
|![](graficos/BufferSize-parte2-caso1(0.5).png)|![](graficos/Delay-parte2-caso1(0.5).png)|
|![](graficos/BufferSize-parte2-caso1(0.1).png)|![](graficos/Delay-parte2-caso1(0.1).png)|

### RESULTADOS CASO 2
| Buffer| delay | HopCount |
| ------ | ------ | ------ |
|![](graficos/BufferSize-parte2-caso2(1).png)|![](graficos/Delay-parte2-caso2(1).png)|![](graficos/HopCount-parte2-caso2(1).png)||
|![](graficos/BufferSize-parte2-caso2(0.5).png)|![](graficos/Delay-parte2-caso2(0.5).png)|![](graficos/HopCount-parte2-caso2(0.5).png)||
|![](graficos/BufferSize-parte2-caso2(0.1).png)|![](graficos/Delay-parte2-caso2(0.1).png)|![](graficos/HopCount-parte2-caso2(0.1).png)||

### PREGUNTAS A RESPONDER
__¿Cuánto mejoran las métricas? ¿Por qué?__

Con la nueva estrategia, las métricas mejoran bastante. El delay y la cantidad de saltos bajan porque los paquetes ya no dan toda la vuelta al anillo, sino que toman el camino más corto. Además, los buffers de los nodos no se llenan tanto, porque el tráfico se reparte mejor y no se acumula todo en un solo nodo como antes. Esto pasa porque ahora cada nodo puede elegir por dónde mandar los paquetes, y el nodo 1 incluso alterna la dirección, lo que ayuda a balancear la carga.

__¿Hay loops de enrutamiento?__

No, con esta estrategia no hay loops. Los paquetes siempre avanzan hacia el destino y no quedan dando vueltas en la red. Cada nodo tiene reglas claras para decidir por dónde mandar el paquete, así que no se repiten caminos innecesarios.

__¿Ves alguna manera de mejorar más aún el diseño?__

Sí, una forma que pensamos es que los nodos pudieran ver si un camino está congestionado y elegir el menos ocupado en ese momento, en vez de seguir siempre la misma regla. 

## OBSERVACIONES
Tuvimos demasiadas complicaciones con Omnet, dificultades a la hora de graficar y demoramos demasiado en eso debido a que no nos funcionaban en ninguna pc.

## SDN (Software-Defined Networking)

El experimento que realizamos en este laboratorio, donde se evalúa el rendimiento de una red en anillo bajo diferentes configuraciones de tráfico, puede ser relacionado con los principios SDN, ya que introduce una separación entre el plano de control y el plano de datos en las redes, lo que permite una gestión más flexible y eficiente del tráfico.

Hoy en día, SDN es clave en redes modernas como centros de datos y telecomunicaciones, ya que mejora la eficiencia del tráfico, reduce costos y facilita la integración de tecnologías como NFV e IoT.

Scott Shenker es uno de los pioneros en el campo de SDN. Su trabajo ha sido fundamental para definir los conceptos de separación de planos y control centralizado, que son la base de esta tecnología.