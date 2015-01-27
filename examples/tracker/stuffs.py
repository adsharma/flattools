# -*- coding: utf-8 -*-

import contextlib
import time
import uuid

from thriftpy import load
from thriftpy.transport import TSocket, TBufferedTransportFactory, \
    TTransportException, TServerSocket
from thriftpy.protocol import TBinaryProtocolFactory
from thriftpy.thrift import TTrackedClient, TTrackedProcessor, \
    TProcessorFactory
from thriftpy.server import TThreadedServer
from thriftpy.trace.tracker import Tracker

thrift = load("animal.thrift")


class NodeTracker(Tracker):
    def __init__(self):
        self.transactions = []

    def pre_handle(self, header):
        self.transactions.append(header)

    def handle(self, header, status):
        trans = self.transactions.pop()
        trans.end = int(time.time() * 1000)
        trans.status = status
        print(trans.__dict__)

    def gen_header(self, header):
        header.request_id = str(uuid.uuid4())
        header.client = "example_client"
        header.start = int(time.time() * 1000)
        header.seq = 0
        header.parent_id = ''

        if self.transactions:
            trans = self.transactions[-1]
            header.parent_id = trans.request_id
            header.seq = trans.seq + 1


tracker = NodeTracker()


class Server(TThreadedServer):
    def __init__(self, processor_factory, trans, trans_factory, prot_factory):
        self.daemon = False
        self.processor_factory = processor_factory
        self.trans = trans

        self.itrans_factory = self.otrans_factory = trans_factory
        self.iprot_factory = self.oprot_factory = prot_factory
        self.closed = False

    def handle(self, client):
        processor = self.processor_factory.get_processor()
        itrans = self.itrans_factory.get_transport(client)
        otrans = self.otrans_factory.get_transport(client)
        iprot = self.iprot_factory.get_protocol(itrans)
        oprot = self.oprot_factory.get_protocol(otrans)
        try:
            while True:
                processor.process(iprot, oprot)
        except TTransportException:
            pass
        except Exception:
            raise

        itrans.close()
        otrans.close()


@contextlib.contextmanager
def client():
    socket = TSocket("localhost", 34567)
    trans = TBufferedTransportFactory().get_transport(socket)
    proto = TBinaryProtocolFactory().get_protocol(trans)
    trans.open()
    cli = TTrackedClient(tracker, thrift.Eating, proto)
    try:
        yield cli
    finally:
        trans.close()


def server():
    processor = TProcessorFactory(thrift.Eating, Handler(), tracker,
                                  TTrackedProcessor)
    server_socket = TServerSocket(host="localhost", port=34567)
    server = Server(processor, server_socket,
                    prot_factory=TBinaryProtocolFactory(),
                    trans_factory=TBufferedTransportFactory())
    return server


class Handler(object):
    def ping(self):
        print('pong')

    def eat_grass(self, sh):
        grass = thrift.Grass()
        grass.name = "mary"
        grass.category = "plant"
        return grass

    def eat_sheep(self, lion):
        sheep = thrift.Sheep()
        sheep.name = "tom"
        sheep.age = 43
        return sheep

    def eat(self, lion):
        with client() as c:
            sheep = c.eat_sheep(lion)
            grass = c.eat_grass(sheep)
            return grass.name