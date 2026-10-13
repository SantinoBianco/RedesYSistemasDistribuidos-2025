#ifndef TRANSPORTTX
#define TRANSPORTTX

#include <omnetpp.h>

using namespace omnetpp;

class TransportTx : public cSimpleModule {
private:
    cQueue buffer;
    cMessage* endService = nullptr;
    int bufferSize;

public:
    TransportTx();
    ~TransportTx();
protected:
    void initialize() override;
    void handleMessage(cMessage* msg) override;
};

Define_Module(TransportTx);

TransportTx::TransportTx() {}

TransportTx::~TransportTx() {
    cancelAndDelete(endService);
}

void TransportTx::initialize() {
    buffer.setName("txBuffer");
    endService = new cMessage("endService");
    bufferSize = par("bufferSize");
}

void TransportTx::handleMessage(cMessage* msg) {
    if (msg == endService) {
        if (!buffer.isEmpty()) {
            cPacket* pkt = check_and_cast<cPacket*>(buffer.pop());
            send(pkt, "toOut$o");
            scheduleAt(simTime() + pkt->getDuration(), endService);
        }
    } else {
        if (buffer.getLength() >= bufferSize) {
            delete msg;
            EV << "TransportTx: buffer full, packet dropped\n";
        } else {
            buffer.insert(msg);
            if (!endService->isScheduled()) {
                scheduleAt(simTime(), endService);
            }
        }
    }
}

#endif
