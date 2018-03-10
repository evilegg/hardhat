#!/usr/bin/env python

import os

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

    reactor.callWhenRunning(spawn_and_terminate)
    reactor.run()


if '__main__' == __name__:
    main()
