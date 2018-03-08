#!/usr/bin/env python

import click

from twisted.internet import protocol
from twisted.internet import reactor


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

    def processExited(self, reason):
        click.echo("processExited, status %s" % (reason.value.exitCode,))

    def processEnded(self, reason):
        click.echo("processEnded, status %s" % (reason.value.exitCode,))
        reactor.stop()


if '__main__' == __name__:
    pp = ClaymoreProtocol()
    def spawn_and_terminate():
        reactor.spawnProcess(pp,
            "eth+sia",
            ["eth+sia"],
            {"WORKER": 'test'})
        reactor.callLater(10.0, pp.transport.loseConnection)

    reactor.callWhenRunning(spawn_and_terminate)
    reactor.run()
