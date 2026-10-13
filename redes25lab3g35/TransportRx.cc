#ifndef TRANSPORTRX
#define TRANSPORTRX

#include <omnetpp.h>

using namespace omnetpp;

class TransportRx : public cSimpleModule {
private:
    cQueue buffer;
    cMessage* endService = nullptr;
    int bufferSize;

public:
    TransportRx();
    ~TransportRx();
protected:
    void initialize() override;
    void handleMessage(cMessage* msg) override;
};

Define_Module(TransportRx);

TransportRx::TransportRx() {}

TransportRx::~TransportRx() {
    cancelAndDelete(endService);
}

void TransportRx::initialize() {
    buffer.setName("rxBuffer");
    endService = new cMessage("endService");
    bufferSize = par("bufferSize");
}

void TransportRx::handleMessage(cMessage* msg) {
    if (msg == endService) {
        if (!buffer.isEmpty()) {
            cPacket* pkt = check_and_cast<cPacket*>(buffer.pop());

            cChannel* chan = gate("toOut$o")->getChannel();
            simtime_t availableTime = chan ? chan->getTransmissionFinishTime() : simTime();
            if (simTime() >= availableTime) {
                send(pkt->dup(), "toOut$o");
                send(pkt, "toApp");
                scheduleAt(simTime() + pkt->getDuration(), endService);
            } else {
                buffer.insert(pkt);
                scheduleAt(availableTime, endService);
            }
        }
    } else {
        if (buffer.getLength() >= bufferSize) {
            delete msg;
            EV << "TransportRx: buffer full, packet dropped\n";
        } else {
            buffer.insert(msg);
            if (!endService->isScheduled()) {
                scheduleAt(simTime(), endService);
            }
        }
    }
}

#endif
