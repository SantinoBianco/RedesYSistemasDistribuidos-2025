#include <string.h>
#include <omnetpp.h>
#include "packet_m.h"

using namespace omnetpp;

class Lnk: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;      // Vector de tamaño de buffer (utilización del buffer)
    cOutVector linkUtilizationVector; // Vector de utilización del enlace
    simsignal_t bufferSizeSignal;
    simsignal_t sentSignal;
    Packet *currentPacket;
public:
    Lnk();
    virtual ~Lnk();
protected:
    virtual void initialize() override;
    virtual void finish() override;
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(Lnk);

Lnk::Lnk() {
    endServiceEvent = nullptr;
    currentPacket = nullptr;
}

Lnk::~Lnk() {
    cancelAndDelete(endServiceEvent);
}

void Lnk::initialize() {
    endServiceEvent = new cMessage("endService");
    bufferSizeVector.setName("BufferSize");           // Utilización del buffer
    linkUtilizationVector.setName("LinkUtilization"); // Utilización del enlace
    bufferSizeSignal = registerSignal("bufferSize");
    sentSignal = registerSignal("packetsSent");
}

void Lnk::finish() {}

void Lnk::handleMessage(cMessage *msg) {
    if (msg == endServiceEvent) {
        if (!buffer.isEmpty()) {
            Packet* pkt = check_and_cast<Packet*>(buffer.pop());
            bufferSizeVector.record(buffer.getLength());      // Registrar tamaño del buffer
            send(pkt, "toOut$o");
            emit(sentSignal, 1);
            linkUtilizationVector.record(1);                 // Registrar utilización del enlace (1 paquete enviado)
            currentPacket = nullptr;
            serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    } else {
        if (msg->arrivedOn("toNet$i")) {
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());      // Registrar tamaño del buffer al recibir un paquete
            if (!endServiceEvent->isScheduled()) {
                scheduleAt(simTime(), endServiceEvent);
            }
        } else {
            // Mensaje desde fuera, reenviar a la red
            send(msg, "toNet$o");
        }
    }
}