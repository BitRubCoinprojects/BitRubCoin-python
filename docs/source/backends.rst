Backends
========

Backends are the protocols and methods used to communicate with the Sumokoin daemon and interact with
the wallet. As of the time of this writing, the only backends available in this library are:

 * ``jsonrpc`` for the HTTP based RPC server,
 * ``offline`` for running the wallet without Internet connection and even without the wallet file.

JSON RPC
----------------

This backend requires a running ``sumo-wallet-rpc`` process with a Sumokoin wallet file opened.
This can be on your local system or a remote node, depending on where the wallet file lives and
where the daemon is running. Refer to the quickstart for general setup information.

The Python `requests`_ library is used in order to facilitate HTTP requests to the JSON RPC
interface. It makes POST requests and passes proper headers, parameters, and payload data as per
the official `Wallet RPC`_ documentation.

.. _`requests`: http://docs.python-requests.org/

.. _`Wallet RPC`: https://getsumokoin.org/resources/developer-guides/wallet-rpc.html

.. automodule:: sumokoin.backends.jsonrpc
   :members:

Offline
----------------

This backend allows creating a `Wallet` instance without network connection or even without the
wallet itself.
