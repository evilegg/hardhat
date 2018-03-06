# hardhat
<img src="assets/speleo-helmet2.svg" width="100" height="100"/>

ETH miner process manager and network proxy

This application is a process manager and network proxy that wraps an Ethereum mining binary and exports metrics and configuration.

The goals of this application are:
1. export metrics to a prometheus stack
1. support stop/start actions
1. add web-based configuration
1. add auto-discovery of miners
1. act as a network proxy and local miner pool
