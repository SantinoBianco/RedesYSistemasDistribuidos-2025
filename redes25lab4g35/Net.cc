#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    int toggleGate = 0; // Alternador para node 1
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
}

void Net::finish() {
}

void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;// Convierte el mensaje recibido en un puntero a Packet

    /*
    // If this node is the final destination, send to App
    if (pkt->getDestination() == this->getParentModule()->getIndex()) {
        send(msg, "toApp$o");
    }
    // If not, forward the packet to some else... to who?
    else {
        // We send to link interface #0, which is the
        // one connected to the clockwise side of the ring
        // Is this the best choice? are there others?
        pkt->setHopCount(pkt->getHopCount() + 1); //antes de reenviar un paquete, estés incrementando el campo hopCount:
        send(msg, "toLnk$o", 0);
    }
    */
    // PARTE 2
    // Obtiene el índice de este nodo en la red
    int myIndex = this->getParentModule()->getIndex();

    // Obtiene el destino del paquete
    int dest = pkt->getDestination();

    // Si el paquete llegó a su destino final (este nodo)
    if (dest == myIndex) {
        // Envía el paquete a la aplicación local (App)
        send(msg, "toApp$o");
    } else {
        // Si el paquete no es para este nodo, hay que reenviarlo
        int gateIndex = 0; // Por defecto, gate 0 (sentido horario)

        // Si el nodo es 0, 6 o 7, siempre reenvía por el gate 0 (horario)
        if (myIndex == 0 || myIndex == 6 || myIndex == 7) {
            gateIndex = 0; // sentido horario
        }
        // Si el nodo es 2, 3 o 4, siempre reenvía por el gate 1 (antihorario)
        else if (myIndex == 2 || myIndex == 3 || myIndex == 4) {
            gateIndex = 1; // sentido antihorario
        }
        // Si el nodo es 1, alterna entre gate 0 y gate 1 en cada reenvío
        else if (myIndex == 1) {
            gateIndex = toggleGate;      // Usa el valor actual de toggleGate (0 o 1)
            toggleGate = 1 - toggleGate; // Cambia toggleGate para la próxima vez (alterna)
        }

        // Incrementa el contador de saltos del paquete
        pkt->setHopCount(pkt->getHopCount() + 1);
        // Reenvía el paquete por el gate seleccionado (0: horario, 1: antihorario)
        send(msg, "toLnk$o", gateIndex);
    }
    
}  

