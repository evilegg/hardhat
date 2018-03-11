#!/usr/bin/env python

import os

import click

from prometheus_client import ProcessCollector
from prometheus_client.twisted import MetricsResource

from twisted.internet import protocol
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource


class ClaymoreProtocol(protocol.ProcessProtocol):
    def outReceived(self, data):
        prefix = click.style('stdout: ', fg='green', bold=True)
        for line in data.split('\n'):
            click.echo(prefix, nl=False)
            click.echo(line)

    def errReceived(self, data):
        prefix = click.style('stderr: ', fg='red', bold=True)
        for line in data.split('\n'):
            click.echo(prefix, nl=False)
            click.echo(line)

    def connectionMade(self):
        click.echo('PID=%s' % self.pid)
        ProcessCollector(namespace='miner', pid=lambda: self.transport.pid)

    def processExited(self, reason):
        click.echo("processExited, status %s" % (reason.value.exitCode,))

    def processEnded(self, reason):
        click.echo("processEnded, status %s" % (reason.value.exitCode,))
        reactor.stop()

@click.command()
@click.option('--executable', help='mining application')
@click.option('--worker', default='test', help='name for this worker')
@click.option('--timeout', default=10.0)
def main(executable, worker, timeout):
    def spawn_and_terminate():
        pp = ClaymoreProtocol()
        reactor.spawnProcess(pp,
                             executable,
                             [os.path.basename(executable)],
                             {'WORKER': worker})
        if timeout > 0.0:
            reactor.callLater(timeout, pp.transport.loseConnection)

    root = Resource()
    root.putChild(b'metrics', MetricsResource())
    factory = Site(root)
    reactor.listenTCP(10999, factory)

    reactor.callWhenRunning(spawn_and_terminate)
    reactor.run()


if '__main__' == __name__:
    main()
